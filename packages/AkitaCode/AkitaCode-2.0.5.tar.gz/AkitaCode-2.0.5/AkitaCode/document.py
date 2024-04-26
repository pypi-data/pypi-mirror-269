
from .line import *
from .bd import *
from pathlib import Path
from .protocol import Protocol, Vector
from .conditionals import generate_combinations
from .messages import StatusMessage, EOPMessage
import pickle
import time
from queue import Queue

VERSION = "2.0.3"


class Document(object):
    """
    La classe ``Document`` permet comprovar ràpidament la sintaxi dels documents de testeig i generar un testbench binari executable. Aquest mòdul requereix la classe "Line" (veure :doc:`mòdul Line <line>`), la qual també està documentada i pot gestionar la informació continguda en un objecte de la classe "Line" eficientment.
    """

    def __init__(self, file="", db="") -> None:
        """
        Inicialitzador de la classe Document.
        """
        self._error = False
        self._error_msg = None
        self.__document: list[Instance] = []
        self.__db = None
        self.__protocol_id = None
        if not Path(file).exists():
            self._error = True
            self._error_msg = StatusMessage(
                msgtype="PathError",
                msg=f"The selected file '{str(Path(file))}' does not exist or is not accessible at this time.",
                return_code=4)
        else:
            if not Path(db).exists():
                self._error = True
                self._error_msg = StatusMessage(
                    msgtype="DatabaseError",
                    msg=f"The specified database path '{str(Path(db))}' does not exist, is corrupt, or is not currently accessible.",
                    return_code=5
                )
            else:
                self.__db = Database(db)
                with open(file, "r") as f:
                    nline = 1
                    for l in f:
                        line_instance = Line(n=nline, line=l)
                        if not line_instance.have_error():
                            converted_instance = line_instance.convert()
                            if converted_instance.is_error():
                                self._error = True
                                self._error_msg = converted_instance.get_error()
                                self.__document = []
                                break
                            else:
                                self.__document += [converted_instance]
                                nline += 1
                        else:
                            self._error = True
                            self._error_msg = line_instance.get_error()
                            self.__document = []
                            break



    def check_syntax(self, q: Queue) -> int:
        """
        Comprova l'estrucura a nivell de document. <q> és una cua de missatges multiprocés.
        :return: True si l'estructura és vàlida, False altrament.
        :rtype: bool
        """
        for_instance:ForInstance = None
        time_statement = False
        level = 0
        if self._error:
            q.put(self._error_msg)
            return self._error_msg.return_code
        for instance in self.__document:
            if isinstance(instance, SkipInstance):
                pass
            elif level == 0:
                if isinstance(instance, ProtocolInstance):
                    level += 1
                else:
                    q.put(
                        StatusMessage(
                            msgtype="StructureError",
                            msg="Protocol needs to be defined before other statements.",
                            return_code=8,
                            nline=instance.nline)
                    )
                    return 8

            elif level == 1:
                if isinstance(instance, EnviromentInstance):
                    level += 1
                elif isinstance(instance,ForInstance):
                    level += 3
                    for_instance = instance
                else:
                    if isinstance(instance, SituationInstance):
                        q.put(
                            StatusMessage(
                                msgtype="StructureError",
                                msg="Cannot declare a Situation without first declaring an Environment statement.",
                                return_code=9,
                                nline=instance.nline)
                        )
                        return 9
                    else:
                        q.put(
                            StatusMessage(
                                msgtype="StructureError",
                                msg="Statement not expected.",
                                return_code=10,
                                nline=instance.nline)
                        )
                        return 10

            elif level == 2:
                if isinstance(instance, SituationInstance):
                    level += 1
                elif isinstance(instance, EndInstance):
                    level -= 1
                else:
                    q.put(
                        StatusMessage(
                            msgtype="StructureError",
                            msg="Statement not expected.",
                            return_code=11,
                            nline=instance.nline)
                    )
                    return 11

            elif level == 3:
                if isinstance(instance, EndInstance):
                    level -= 1
                elif isinstance(instance, (VariableInstance, FunctionInstance)):
                    pass
                else:
                    q.put(
                        StatusMessage(
                            msgtype="StructureError",
                            msg="Statement not expected.",
                            return_code=12,
                            nline=instance.nline)
                    )
                    return 12
                
            elif level == 4:
                if isinstance(instance,TimeInstance):
                    time_statement = True
                    level += 1
                else:
                    q.put(
                        StatusMessage(
                            msgtype="StructureError",
                            msg="Statement not expected.",
                            return_code=13,
                            nline=instance.nline)
                    )
                    return 13
            
            elif level == 5:
                if isinstance(instance,(VariableInstance, FunctionInstance)):
                    if time_statement:
                        for_instance.nsituations += 1 
                    time_statement = False

                elif isinstance(instance,TimeInstance):
                    if time_statement:
                        q.put(
                            StatusMessage(
                                msgtype="StructureError",
                                msg="Time instance not expected after another Time instance.",
                                return_code=14,
                                nline=instance.nline)
                        )
                        return 14
                    else:
                        time_statement = True
                elif isinstance(instance, EndInstance):
                    if time_statement:
                        q.put(
                            StatusMessage(
                                msgtype="StructureError",
                                msg="End instance not expected after Time instance. Must be declare variables or functions before End instance after Time instance.",
                                return_code=15,
                                nline=instance.nline)
                        )
                        return 15
                    else:
                        for_instance = None
                        level -= 4
                else:
                    q.put(
                        StatusMessage(
                            msgtype="StructureError",
                            msg="Statement not expected.",
                            return_code=16,
                            nline=instance.nline)
                    )
                    return 16     
        if level == 1:
            q.put(
                StatusMessage(
                    msgtype="Success",
                    msg="No errors detected during structuration phase.",
                    return_code=1
                    )
                )
            return 1
        q.put(
            StatusMessage(
                msgtype="UnexpectedError",
                msg="The structuring process ended unexpectedly.",
                return_code=17
                )
            )
        return 17



    def check_spell(self, q:Queue) -> int:
        """
        Comprova que la informació facilitada per l'usuari sigui correcta, vàlida i coherent.
        """
        # Variables que s'accepten com a valors (han d'estar definides prèviament abans de ser usades i han de ser de tipus TX).
        layer = 0
        inside_for = False
        const_vars:dict = {}
        for instance in self.__document:
            if isinstance(instance, ProtocolInstance):
                p_id = self.__db.get_protocol_id(instance.name)
                if p_id is not None:
                    self.__protocol_id = p_id
                else:
                    q.put(
                        StatusMessage(
                            msgtype="ProtocolError",
                            msg=f"The ''{instance.name}'' protocol not exist on database.",
                            return_code=18,
                            nline=instance.nline
                        )
                    )
                    return 18

            elif isinstance(instance, VariableInstance):
                v_id = self.__db.get_variable_id(
                    p_id=self.__protocol_id, v_name=instance.name)
                if v_id is False:
                    q.put(
                        StatusMessage(
                            msgtype="VariableError",
                            msg=f"Variable ''{instance.name}'' is not defined in ''{self.__db.get_protocol_name(self.__protocol_id)}'' protocol.",
                            return_code=19,
                            nline=instance.nline
                        )
                    )
                    return 19
                instance.ids = v_id
                v_info = self.__db.get_info_from_variable(v_id)
                nbits: str = v_info["variable_mask"]
                nbits = nbits.count("1")
                instance.is_response = True if v_info["variable_direction"] == 1 else False
                if instance.value is None:
                    instance.value = v_info["variable_default"]
                try:
                    if not isinstance(instance.value,int):
                        v_value:int = int(instance.value,0)
                    else:
                        v_value = instance.value
                    instance.value = v_value
                    if nbits > 1:
                        mult = int(v_info["variable_mul"])
                        div = int(v_info["variable_div"])
                        offset = int(v_info["variable_offset"])
                        v_value = int((v_value*mult)/div)+offset
                        # Cal comprovar si el valor hi té cabuda.
                        if v_info["variable_is_signed"] == 1:
                            if v_value not in range(-2**(nbits-1), 2**(nbits-1)):
                                q.put(
                                    StatusMessage(
                                        msgtype="ValueError",
                                        msg=f"Value {v_value} exceeds minimum or maximum {instance.name} value. Overflow!",
                                        return_code=20,
                                        nline=instance.nline
                                    )
                                )
                                return 20
                        else:
                            if v_value not in range(0, 2**(nbits)):
                                q.put(
                                    StatusMessage(
                                        msgtype="ValueError",
                                        msg=f"Value {v_value} exceeds minimum or maximum {instance.name} value. Overflow!",
                                        return_code=21,
                                        nline=instance.nline
                                    )
                                )
                                return 21

                        if v_info["variable_direction"] == 0:
                            const_vars[instance.name] = instance.value

                    elif nbits == 1:
                        if v_value not in range(0, 2):
                            q.put(
                                StatusMessage(
                                    msgtype="ValueError",
                                    msg=f"Value {v_value} exceeds minimum or maximum {instance.name} value. Overflow!",
                                    return_code=22,
                                    nline=instance.nline
                                )
                            )
                            return 22

                        if v_info["variable_direction"] == 0:
                            const_vars[instance.name] = instance.value

                    else:
                        q.put(
                            StatusMessage(
                                msgtype="ValueError",
                                msg=f"Unexpected number of bits.",
                                return_code=23,
                                nline=instance.nline
                            )
                        )
                        return 23
                except:
                    v_value:str = instance.value
                    # print(v_value)
                    if (v_value == "True" and nbits == 1) or (v_value == "False" and nbits == 1) or (v_value is None):
                        instance.value = 1 if v_value == "True" else 0
                        const_vars[instance.name] = instance.value
                    elif (v_value == "True" and nbits != 1) or (v_value == "False" and nbits != 1):
                        q.put(
                            StatusMessage(
                                msgtype="ValueError",
                                msg=f"Value ''{v_value}'' is only valid for boolean variables. Evaluated variable is {instance.name}.",
                                return_code=24,
                                nline=instance.nline
                            )
                        )
                        return 24
                    elif v_value in list(const_vars.keys()):
                        # Busquem la informació de la variable de la qual es vol afegir el valor.
                        # Han de compartir tipus, signe i longitud. En cas contrari, haurà de donar error.
                        value_variable_id = self.__db.get_variable_id(
                            p_id=self.__protocol_id, v_name=v_value)
                        value_variable_info = self.__db.get_info_from_variable(
                            v_id=value_variable_id)
                        value_nbits: str = value_variable_info["variable_mask"]
                        if value_variable_info["variable_direction"] == 1:
                            q.put(
                                StatusMessage(
                                    msgtype="ValueError",
                                    msg=f"Value of {v_value} cannot be used as the value of variable {instance.name} because output assignment is not allowed.",
                                    return_code=25,
                                    nline=instance.nline
                                )
                            )
                            return 25
                        if value_nbits.count("1") != nbits:
                            q.put(
                                StatusMessage(
                                    msgtype="ValueError",
                                    msg=f"Value of {v_value} cannot be used as the value of variable {instance.name} because they differ in bit length.",
                                    return_code=26,
                                    nline=instance.nline
                                )
                            )
                            return 26
                        if value_variable_info["variable_is_signed"] != v_info["variable_is_signed"]:
                            q.put(
                                StatusMessage(
                                    msgtype="ValueError",
                                    msg=f"Value of {v_value} cannot be used as the value of variable {instance.name} because they differ in the type of variable.",
                                    return_code=27,
                                    nline=instance.nline
                                )
                            )
                            return 27
                        if not inside_for:
                            instance.value = const_vars[v_value]
                        const_vars[instance.name] = instance.value
                    elif v_value not in list(const_vars.keys()):
                        q.put(
                            StatusMessage(
                                msgtype="AssignmentError",
                                msg=f"Value ''{v_value}'' is not defined previously and cannot be assigned.",
                                return_code=28,
                                nline=instance.nline
                            )
                        )
                        return 28
                    else:
                        q.put(
                            StatusMessage(
                                msgtype="ValueError",
                                msg=f"Value {v_value} on variable ''{instance.name}'' is not a valid value.",
                                return_code=29,
                                nline=instance.nline
                            )
                        )
                        return 29

            elif isinstance(instance, FunctionInstance):
                # Busquem l'identificació de la funció amb el nom de la instància funció.
                f_id = self.__db.get_function_id(p_id=self.__protocol_id,f_name=instance.name)
                # Si no existeix llançem error i retornem False.
                if f_id is None:
                    q.put(
                        StatusMessage(
                            msgtype="FunctionError",
                            msg=f"Function ''{instance.name}'' is not defined in ''{self.__protocol_id}'' protocol.",
                            return_code=30,
                            nline=instance.nline
                        )
                    )
                    return 30
                # Si la funció existeix obtemim els arguments que conté i els comparem amb els que té la instáncia.
                instance.ids = f_id
                f_args = self.__db.get_arguments_from_function(f_id)
                instance_len = len(instance.arguments.keys())
                args_len = len(f_args)
                # Comprovem el nombre d'arguments esperats.
                if instance_len != args_len:
                    q.put(
                        StatusMessage(
                            msgtype="FunctionError",
                            msg=f"Function ''{instance.name}'' have {args_len} arguments but given {instance_len}. Number of arguments mismatch.",
                            return_code=31,
                            nline=instance.nline
                        )
                    )
                    return 31
                # Si coincideixen el nombre d'arguments amb els de la instància, comprovem si existeixen per la funció objectiu.
                for arg in instance.arguments.keys():
                    if arg not in f_args:
                        q.put(
                            StatusMessage(
                                msgtype="ArgumentError",
                                msg=f"Argument ''{arg}'' is not a valid argument for {instance.name} function. Possible arguments must be: {f_args}.",
                                return_code=32,
                                nline=instance.nline
                            )
                        )
                        return 32
                    else:
                        # Processem la informació de cada un dels arguments.
                        a_id = self.__db.get_argument_id(
                            f_id=f_id, a_name=arg)
                        if a_id is None:
                            q.put(
                                StatusMessage(
                                    msgtype="ArgumentError",
                                    msg=f"Argument ''{arg}'' is not defined in ''{instance.name}'' function.",
                                    return_code=33,
                                    nline=instance.nline
                                )
                            )
                            return 33
                        arg_info = self.__db.get_info_from_argument(a_id)
                        arg_name = arg_info["argument_name"]
                        nbits: str = arg_info["argument_mask"]
                        nbits = nbits.count("1")
                        try:
                            arg_value = int(instance.arguments[arg],0)
                            instance.arguments[arg] = arg_value
                            if nbits > 1:
                                mult = int(arg_info["argument_mul"])
                                div = int(arg_info["argument_div"])
                                offset = int(arg_info["argument_offset"])
                                arg_value = int((arg_value*mult)/div)+offset
                                # Cal comprovar si el valor hi té cabuda.
                                if arg_info["argument_is_signed"] == 1:
                                    if arg_value not in range(-2**(nbits-1), 2**(nbits-1)):
                                        q.put(
                                            StatusMessage(
                                                msgtype="ValueError",
                                                msg=f"Value {arg_value} exceeds minimum or maximum {arg_name} argument value. Overflow!",
                                                return_code=34,
                                                nline=instance.nline
                                            )
                                        )
                                        return 34
                                else:
                                    if arg_value not in range(0, 2**(nbits)):
                                        q.put(
                                            StatusMessage(
                                                msgtype="ValueError",
                                                msg=f"Value {arg_value} exceeds maximum {arg_name} argument value. Overflow!",
                                                return_code=35,
                                                nline=instance.nline
                                            )
                                        )
                                        return 35

                            elif nbits == 1:
                                if arg_value not in range(0, 2):
                                    q.put(
                                        StatusMessage(
                                            msgtype="ValueError",
                                            msg=f"Value {arg_value} exceeds maximum {arg_name} argument value. Overflow!",
                                            return_code=36,
                                            nline=instance.nline
                                        )
                                    )
                                    return 36

                            else:
                                q.put(
                                    StatusMessage(
                                        msgtype="ValueError",
                                        msg=f"Unexpected number of bits.",
                                        return_code=37,
                                        nline=instance.nline
                                    )
                                )
                                return 37
                        except:
                            v_value = instance.arguments[arg]
                            if (v_value == "True" and nbits.count("1") == 1) or (v_value == "False" and nbits.count("1") == 1) or (v_value is None):
                                instance.arguments[arg] = 1 if v_value == "True" else 0
                            elif v_value in list(const_vars.keys()):
                                # Busquem la informació de la variable de la qual es vol afegir el valor.
                                # Han de compartir tipus, signe i longitud. En cas contrari, haurà de donar error.
                                value_variable_id = self.__db.get_variable_id(
                                    p_id=self.__protocol_id, v_name=v_value)
                                value_variable_info = self.__db.get_info_from_variable(
                                    v_id=value_variable_id)
                                value_nbits: str = value_variable_info["variable_mask"]
                                if value_variable_info["variable_direction"] == 1:
                                    q.put(
                                        StatusMessage(
                                            msgtype="ValueError",
                                            msg=f"Value of {arg_value} cannot be used as the value of argument {arg_name} because output assignment is not allowed.",
                                            return_code=38,
                                            nline=instance.nline
                                        )
                                    )
                                    return 38
                                if value_nbits.count("1") != nbits:
                                    q.put(
                                        StatusMessage(
                                            msgtype="ValueError",
                                            msg=f"Value of {arg_value} cannot be used as the value of argument {arg_name} because they differ in bit length.",
                                            return_code=39,
                                            nline=instance.nline
                                        )
                                    )
                                    return 39
                                if value_variable_info["variable_is_signed"] != arg_info["argument_is_signed"]:
                                    q.put(
                                        StatusMessage(
                                            msgtype="ValueError",
                                            msg=f"Value of {v_value} cannot be used as the value of argument {arg_name} because they differ in the type of variable.",
                                            return_code=40,
                                            nline=instance.nline
                                        )
                                    )
                                    return 40
                                if not inside_for:
                                    instance.arguments[arg] = const_vars[v_value]
                            elif v_value not in list(const_vars.keys()):
                                q.put(
                                    StatusMessage(
                                        msgtype="AssignmentError",
                                        msg=f"Value {v_value} is not defined previously and cannot be assigned.",
                                        return_code=41,
                                        nline=instance.nline
                                    )
                                )
                                return 41
                            else:
                                q.put(
                                    StatusMessage(
                                        msgtype="ValueError",
                                        msg=f"Value {v_value} on variable ''{arg_name}'' is not a valid value.",
                                        return_code=42,
                                        nline=instance.nline
                                    )
                                )
                                return 42

            elif isinstance(instance, ForInstance):
                inside_for = True
                layer += 1
                for item in instance.iter:
                    v_id = self.__db.get_variable_id(self.__protocol_id,item)
                    if v_id is None:
                        q.put(
                            StatusMessage(
                                msgtype="ValueError",
                                msg=f"Variable ''{item}'' is not defined in ''{self.__db.get_protocol_name(self.__protocol_id)}'' protocol.",
                                return_code=43,
                                nline=instance.nline
                            )
                        )
                        return 43
                    v_info = self.__db.get_info_from_variable(v_id)["variable_direction"]
                    if v_info == 1:
                        q.put(
                            StatusMessage(
                                msgtype="ForVariableError",
                                msg=f"Variable ''{arg_name}'' is defined as input, not as output. For instance not allow input variables.",
                                return_code=44,
                                nline=instance.nline
                            )
                        )
                        return 44
                    const_vars[item] = None                
            
            elif isinstance(instance, EndInstance):
                if (inside_for and layer == 1) or (not inside_for and layer == 2):
                    inside_for = False
                    const_vars = {}
                layer -= 1
            
            elif isinstance(instance, TimeInstance):
                pass
            
            elif isinstance(instance, (EnviromentInstance, SituationInstance)):
                layer += 1
            
            elif isinstance(instance, SkipInstance):
                pass
            
            else:
                q.put(
                    StatusMessage(
                        msgtype="TypeError",
                        msg=f"{str(instance)} is not already defined. Report bug via email to aamat@ausa.com.",
                        return_code=45,
                        nline=instance.nline
                    )
                )
                return 45
        q.put(
            StatusMessage(
                msgtype="Success",
                msg="No errors detected during spell phase.",
                return_code=2
                )
            )
        return 2



    def makec(self,q:Queue,pathname:Path|str,emulate:bool=False,autoclose:bool=False) -> int:
        """
        Crea el document executable per la realització de la validació.
        """
        emu = emulate
        p_id = None
        protocol = None
        exportable = []
        in_for = False
        current_for_situation:int = 0
        for_number_of_situations:int = 0
        for_situations:list[dict]|None = None
        instance_level = 0
        timeTotal = 0
        timeA = time.perf_counter()
        for instance in self.__document:

            if time.perf_counter()-timeA >= 1:
                timeTotal += time.perf_counter()-timeA
                timeA = time.perf_counter()
                # print(timeTotal)

            if isinstance(instance,ProtocolInstance):
                p_id = self.__db.get_protocol_id(instance.name)
                protocol = Protocol(instance.name)
                protocol.import_protocol(
                    db=self.__db,
                    p_id=p_id
                    )
                instance_level += 1

            elif isinstance(instance, EnviromentInstance):
                exportable += [Vector(instance.name,"E",None)]
                instance_level +=1

            elif isinstance(instance, SituationInstance):
                exportable += [Vector(instance.name, "S", instance.time)]
                instance_level +=1

            elif isinstance(instance,VariableInstance):
                if not in_for:
                    exportable += [Vector(ids=instance.ids,data_type="R" if instance.is_response else "T", value=instance.value)]
                else:
                    if isinstance(instance.value,int):
                        for i in range(current_for_situation-1,len(for_situations),for_number_of_situations):
                            for_situations[i][instance.name] = instance.value
                    else:
                        for i in range(current_for_situation-1,len(for_situations),for_number_of_situations):
                            for_situations[i][instance.name] = for_situations[i][instance.value]

            elif isinstance(instance,FunctionInstance):
                if not in_for:
                    exportable += [Vector(instance.ids,"F",None)]
                    for arg in tuple(instance.arguments.keys()):
                        exportable += [Vector(ids=self.__db.get_argument_id(instance.ids,arg),data_type="A",value=instance.arguments[arg])]
                else:
                    # Recorrem el llistat de situacions
                    for i in range(current_for_situation-1,len(for_situations),for_number_of_situations):
                        for_situations[i]["**functions"][instance.name] = {}
                        for argument in tuple(instance.arguments.keys()):
                            if isinstance(instance.arguments[argument],int):
                                for_situations[i]["**functions"][instance.name][argument] = instance.arguments[argument]
                            else:
                                for_situations[i]["**functions"][instance.name][argument] = for_situations[i][instance.arguments[argument]]
                            # Es possible que pugui donar error d'indexació quan s'intenta afegir el valor d'una variable anterior definida a l'hora de passar-ho com argument.
                            # Intentar detectar l'error i, si es possible, manipular-ho amb conseqüència.
                    # #######  Revisar!!

            elif isinstance(instance, EndInstance):
                instance_level -=1
                if in_for:
                    in_for = False
                    curr_env_name = None
                    # Itera per totes les situacions
                    for i in range(0, len(for_situations)):
                        if time.perf_counter()-timeA >= 1:
                            timeTotal += time.perf_counter()-timeA
                            timeA = time.perf_counter()
                            q.put(timeTotal)
                        # Busca la primera situació de cada entorn i inicialitza l'entorn.
                        if i % for_number_of_situations == 0:
                            exportable += [Vector(ids=curr_env_name,data_type="E",value=None)]
                        # Creem una nova situació per cada diccionari de la llista.
                        exportable += [Vector(ids=0,data_type="S",value=for_situations[i]["**time"])]
                        # Cerquem totes les variables
                        sit_variables = [element for element in list(for_situations[i].keys()) if element not in ("**time","**functions")]
                        # Creem els Vectors en funció del tipus de variable.
                        for var in sit_variables:
                            var_id = self.__db.get_variable_id(self.__protocol_id,var)
                            exportable += [Vector(
                                ids=var_id,
                                data_type= "T" if self.__db.get_info_from_variable(var_id)["variable_direction"] == 0 else "R",
                                value=for_situations[i][var])]
                            
                        # Creem els Vectors de les funcions
                        sit_fn = [element for element in list(for_situations[i]["**functions"].keys())]
                            # Si un argument depén d'una variable, s'ha de comprovar.
                        for fn in sit_fn:
                            fn_id = self.__db.get_function_id(self.__protocol_id,fn)
                            exportable += [Vector(
                                ids=fn_id,
                                data_type="F",
                                value=None
                            )]
                            fn_arg_names = self.__db.get_arguments_from_function(fn_id)
                            fn_arg_id = self.__db.get_all_argument_id_from_function(fn_id)
                            for arg in range(len(fn_arg_id)):
                                exportable += [Vector(
                                    ids=fn_arg_id[arg],
                                    data_type="A",
                                    value=for_situations[i]["**functions"][fn][fn_arg_names[arg]]
                                )]

                        

            elif isinstance(instance, ForInstance):
                instance_level += 1
                in_for = True
                current_for_situation = 0
                for_number_of_situations = instance.nsituations
                for_situations = generate_combinations(database=self.__db,
                                                       protocol_id=self.__protocol_id,
                                                       iterlist=instance.iter,
                                                       num_situations=instance.nsituations)
                

            elif isinstance(instance, TimeInstance):
                current_for_situation += 1
                for i in range(current_for_situation-1,len(for_situations),for_number_of_situations):
                    for_situations[i]["**time"] = instance.time
                    
                




        if instance_level == 1:
            the_file = {
                "protocol": protocol,
                "data": exportable,
                "compiler_version": VERSION
            }
            try:
                pickle.dump(the_file,open(str(pathname),"wb"))
                q.put(
                    StatusMessage(
                        msgtype="Success",
                        msg="Make testbench operation completed successfuly.",
                        return_code=0
                        )
                    )
                return 0
            except:
                q.put(
                    StatusMessage(
                        msgtype="MakeError",
                        msg="Operation make failed!",
                        return_code=0
                        )
                    )
                return 3
        else:
            q.put(
                StatusMessage(
                    msgtype="MakeError",
                    msg="Unexpected error occurred during compilation.",
                    return_code=46
                    )
                )
            return 46
        

    def make(self,q:Queue,pathname:Path|str,emulate:bool=False,autoclose:bool=False):
        """
        Compila un fitxer ATD d'AkitaCode.
        """
        fase_A = self.check_syntax(q)
        if fase_A == 1:
            fase_B = self.check_spell(q)
            if fase_B == 2:
                fase_C = self.makec(q,pathname)
                q.put(
                    EOPMessage()
                )
                return fase_C
            q.put(
                EOPMessage()
            )
            return fase_B
        q.put(
            EOPMessage()
        )
        return fase_A


if __name__ == "__main__":
    # Create a database instance.
    # import config_mod
    import queue
    q = queue.Queue()
    # db = config_mod.get_db_path()
    db = "C:/Users/aamat/.akitacan/data.db"
    # Get path of file.
    filename = "prova_for_time"
    in_filename = "E:/Akitacan/dev/AkitaCode/test/{}{}".format(filename,".atd")
    out_filename = "E:/Akitacan/dev/AkitaCode/test/{}{}".format(filename,".akita")

    # Create a document instance.
    doc = Document(in_filename, db)

    # print(doc._error)
    # print(doc._error_msg) if doc._error_msg is not None else print("Success!!")

    fase_A = doc.check_syntax(q)
    print("FASE A: {}".format(fase_A))
    print(q.get())
    if fase_A:
        fase_B = doc.check_spell(q)
        print("FASE B: {}".format(fase_B))
        print(q.get())
        if fase_B:
            fase_C = doc.makec(q,out_filename,autoclose=True)
            print("FASE C: {}".format(fase_C))
            print(q.get())
            if fase_C == 0:
                f = pickle.load(open(out_filename,"rb"))
                f = f["data"]
                for l in f:
                    print(repr(l)+"\r")
                # print(f)
            print(q.get())