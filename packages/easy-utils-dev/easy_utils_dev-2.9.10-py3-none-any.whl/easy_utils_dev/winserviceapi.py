from .uiserver import UISERVER
from .debugger import DEBUGGER
import subprocess
from .utils import generateToken
from flask import request
from traceback import format_exc
import os
import json
import psutil
from threading import Thread
from time import sleep
class WinServiceApi() :
    def __init__(self, debugger_path, port=7718,username='admin' , password='Nokia@2023' ) -> None:
        self.logger = DEBUGGER('WinServiceApi' , homePath=debugger_path)
        self.ui = UISERVER(address='127.0.0.1', port=port,https=True)
        self.services = {}
        self.logger.set_level('debug')
        self.token = 'not-allowed-ever-forever'
        self.username = username
        self.password = password
        pass 

    def run(self) :
        self.ui.startUi(True)
        self.app = self.ui.getFlask()
        self.wrapper()
        self.socket = self.ui.getSocketio()

    def buildReturnCode(self , process) :
        if process.returncode == 1 or process.returncode == None :
            rc = 1
        elif process.returncode == 0 :
            rc = 0
        else:
            rc = 1
        return rc

    def check_pid_running(self , pid):
        if pid == 0 :
            return False
        return psutil.pid_exists(pid)

    def get_child_pids(self , parent_pid):
        self.logger.debug(f'looking for child {parent_pid}')
        cli = f'''wmic process get Caption,ParentProcessId,ProcessId | findstr "{parent_pid}"'''
        a = subprocess.Popen(cli, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, text=True)
        a=a.stdout.readlines()
        for line in a :
            if line.startswith('\n'): continue
            line= line.split(' ')
            line = [x for x in line if x != '' ]
            if str(line[1]) == str(parent_pid) :
                self.logger.debug(f'looking for child {parent_pid} completed.')
                return int(line[2])
        return 0

    def get_process_details(self, pid):
        try:
            # Get process information by PID
            process = psutil.Process(pid)
            # Get process details
            details = {
                'pid': process.pid,
                'name': process.name(),
                'cmdline': process.cmdline(),
                'cpu_percent': process.cpu_percent(),
                'memory_info': process.memory_info(),
                'create_time': process.create_time(),
                'status': process.status(),
                'username': process.username(),
                'connections': process.connections(),
                # Add more details as needed
            }
            return details
        except psutil.NoSuchProcess:
            return {}

    def wrapper(self) :
        
        @self.app.before_request
        def validate() :
            if not '/service/api/winservice/login' in request.url :
                if request.headers.get('Authorization' , 'not-allowed') != self.token :
                    return json.dumps({"status" : 400 , 'message' : 'Invalid Authorization.'})


        @self.app.route('/service/api/winservice/login' , methods=['POST'])
        def get_token() :
            try :
                if request.form.get('username') != self.username or  request.form.get('password') != self.password :
                    raise Exception('Invalid username or password')
                self.token = generateToken(30)
                return json.dumps({"status" : 200 , 'token' : self.token })
            except Exception as error :
                self.logger.error(error)
                self.logger.debug(format_exc())
                return json.dumps({'status' : 400 , 'message' : str(error)})
        @self.app.route('/service/api/winservice/run' , methods=['POST'])
        def api_win_run_service() :
            try :
                serviceName = request.form.get('serviceName')
                serviecPath = request.form.get('servicePath')
                stream = request.form.get('stream' , 'true' )
                autoRestart = request.form.get('autoRestart' , 'true' )
                tries = int(request.form.get('tries' , 3 ))
                command = request.form.get('command' , 'false' )
                id = generateToken(4)
                if command == 'false' :
                    if not os.path.exists(serviecPath) :
                        raise Exception(f'service path does not exist.')
                process = subprocess.Popen(serviecPath, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, text=True)
                pid = self.get_child_pids(process.pid)
                self.logger.info(f"Service {serviceName} is running with main_pid=[{process.pid}] pid=[{pid}]")
                def stream_api() :
                    self.logger.info(f'stream started for {id}')
                    data = self.services[id]
                    data['stream_started'] = True
                    process = data.get('process')
                    for line in process.stdout:
                        d= json.dumps({'line' : line.strip()})
                        self.logger.debug(d)
                        data['buffer'] += line.strip() + '\n'
                        if stream == 'true' : 
                            self.socket.emit( f"{id}" , d )
                    process.terminate()
                    self.logger.info(f'stream process with {data.get("pid")} terminated.')
                def auto_restart(id) :
                    while True :
                        sleep(2)
                        if self.services[id].get('terminate' , False ) :
                            self.services[id] = {}
                            break
                        process = self.services[id]['process']
                        pid = self.get_child_pids(process.pid)
                        status = self.check_pid_running(pid)
                        self.logger.debug(f'service status for {pid} is running={status}')
                        if self.services[id]['restart_try'] == tries :
                            self.logger.debug(f'service status for {pid} is {status}. maximum restart reached.')
                            break
                        elif not status :
                            self.services[id]['restart_try'] += 1
                            _try = self.services[id]['restart_try']
                            self.logger.info(f'service {id} is down. restarting try={_try}')
                            process.kill()
                            process = subprocess.Popen(serviecPath, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, text=True)
                            self.services[id]['process'] = process
                            self.services[id]['pid'] = pid = self.get_child_pids(process.pid)
                            t = Thread(target=stream_api , args=[])
                            t.start()

                self.services[id] = {'process' : process , 'serviceName' : serviceName , 'stream_started' : False , 'pid' : pid , 'restart_try' : 0, 'buffer' : '' , 'errors': ''  }
                t = Thread(target=stream_api , args=[])
                t.start()
                if autoRestart == 'true' :
                    t = Thread(target=auto_restart , args=[id])
                    t.start()
                return json.dumps({'status' : 200 , 'id' : id })
            except Exception as error :
                self.logger.error(error)
                self.logger.debug(format_exc())
                return json.dumps({'status' : 400 , 'message' : str(error)})

        @self.app.route('/service/api/winservice/status' , methods=['get'])
        def api_win_get_service_status() :
            try :
                try :
                    id = request.args.get('id')
                    data = self.services[id]
                    process = data.get('process')
                    pid = process.pid
                    childs = self.get_child_pids(pid)
                    result = self.check_pid_running(childs)
                    rc = self.buildReturnCode(process)
                except KeyError:
                    result = False
                return json.dumps({'status' : 200 , 'running' : result , 'returncode' : rc })
            except Exception as error :
                self.logger.error(error)
                self.logger.debug(format_exc())
                return json.dumps({'status' : 400 , 'message' : str(error)})

        @self.app.route('/service/api/winservice/stdout' , methods=['get'])
        def api_win_get_service_std() :
            try :
                try :
                    id = request.args.get('id')
                    data = self.services[id]
                    process = data.get('process')
                    rc = self.buildReturnCode(process)
                except KeyError :
                    raise Exception(f'Process with id {id} does not exist.')
                return json.dumps({'status' : 200 , 'stdout' : data.get('buffer' , '').split('\n')  , 'returncode' : rc })
            except Exception as error :
                self.logger.error(error)
                self.logger.debug(format_exc())
                return json.dumps({'status' : 400 , 'message' : str(error)})

        @self.app.route('/service/api/winservice/stop' , methods=['post'])
        def api_win_get_service_stop() :
            try :
                try :
                    id = request.args.get('id')
                    data = self.services[id]
                except KeyError :
                    raise Exception(f'Process with id {id} does not exist.')
                process = data.get('process')
                pid = self.get_child_pids(process.pid)
                data['terminate'] = True
                process.terminate()
                s,o = subprocess.getstatusoutput(f"taskkill /PID {pid} /F")
                return json.dumps({'status' : 200 , 'returncode' : s , 'returntext' : o})
            except Exception as error :
                self.logger.error(error)
                self.logger.debug(format_exc())
                return json.dumps({'status' : 400 , 'message' : str(error)})

        @self.app.route('/service/api/winservice/logging/change' , methods=['POST'])
        def api_win_get_service_log_change() :
            try :
                level = request.form.get('level')
                self.logger.set_level(level)
                return json.dumps({'status' : 200 , 'message' : f'logger trace level changed to {level}' })
            except Exception as error :
                self.logger.error(error)
                self.logger.debug(format_exc())
                return json.dumps({'status' : 400 , 'message' : str(error)})
            
        @self.app.route('/service/api/winservice/logging/change/location' , methods=['POST'])
        def api_win_get_service_log_change_loc() :
            try :
                abpath = request.form.get('location')
                self.logger.changeHomePath(abpath)
                return json.dumps({'status' : 200 , 'message' : f'logger trace path changed to {self.logger.homePath}' })
            except Exception as error :
                self.logger.error(error)
                self.logger.debug(format_exc())
                return json.dumps({'status' : 400 , 'message' : str(error)})
            
        @self.app.route('/service/api/winservice/getdetails' , methods=['GET'])
        def api_win_get_service_log_change_get() :
            try :
                try :
                    id = request.args.get('id')
                    data = self.services[id]
                    process = data.get('process')
                    pid = self.get_child_pids(process.pid)
                except KeyError :
                    raise Exception(f'Process with id {id} does not exist.')
                return json.dumps({'status' : 200 , 'result' : self.get_process_details(pid) })
            except Exception as error :
                self.logger.error(error)
                self.logger.debug(format_exc())
                return json.dumps({'status' : 400 , 'message' : str(error)})
            
        @self.app.route('/service/api/winservice/exec' , methods=['POST'])
        def api_execee() :
            try :
                cli = request.form.get('cli')
                s, r = subprocess.getstatusoutput(cli)
                return json.dumps({'status' : 200 , 'result' : r , 'returncode' : s })
            except Exception as error :
                self.logger.error(error)
                self.logger.debug(format_exc())
                return json.dumps({'status' : 400 , 'message' : str(error)})
