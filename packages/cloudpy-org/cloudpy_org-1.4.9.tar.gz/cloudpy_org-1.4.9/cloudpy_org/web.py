from cloudpy_org import cloudpy_org_version,processing_tools as pt, aws_framework_manager_client
import os
class flask_website:
    def __init__(self,app:object,username_or_email:str,pwd:str,aws_auth_token:str):
        self.app = app
        self.aws = aws_framework_manager_client(
            username_or_email=username_or_email
            ,pwd=pwd
            ,aws_auth_token=aws_auth_token)
        self.create_framework()
    def create_framework(self):
        p = {}
        current_path = os.getcwd() + '/'
        static_folder =  current_path + 'static/'
        templates_folder =  current_path + 'templates/'
        self.create_path(static_folder)
        self.create_path(templates_folder)
        self.path = {}
        self.path['static'] = static_folder
        self.path['templates'] = templates_folder
        self.path["jsons"] = static_folder + '/json/'
        self.path["biscuits"] = static_folder + '/biscuits/'
        self.path["css"] = static_folder + '/css/'
        self.path["js"] = static_folder + '/js/'
        self.path["icons"] = static_folder + '/icons/'
        self.path["images"] = static_folder + '/images/'
        self.path["scss"] = static_folder + '/scss/'
        l = list(self.path.keys())
        l.sort()
        for i in l:
            self.create_path(self.path[i])
    #_________________________________
    def create_path(self,path:str):
        if os.path.exists(path) == False:
            os.mkdir(path)

    def pre_authenticate(username_or_email:str,pwd:str):
        try:
            udat = self.aws.check_if_user_exists_and_was_confirmed(
                username_or_email=[username_or_email]
                ,bucket_name=pt.this_bucket_name)
        except:
            udat = "Invalid user."
        if type(udat) == dict and udat != {}:
            lt = list(udat.keys())
            if "exists" in lt and "confirmed" in lt:
                if udat["exists"]:
                    if udat["confirmed"] == 1:
                        username = udat["file_name"].split("-0-")[0].replace("-1-","@").replace("-2-",".")
                        referenceName = udat["file_name"].replace(".json","")
                        minutes_to_expire = 30
                        token = self.aws.create_token_with_expiration(
                            username=username
                            ,pwd=pwd
                            ,bucket_name=pt.this_bucket_name
                            ,minutes_to_expire=minutes_to_expire)
                        if len(token) > 500 and "error" not in token.lower():
                            resp = self.aws.validate_token(username=username,token=token,bucket_name=pt.this_bucket_name)
                            if "successful request: valid token" in resp.lower():
                                user_data = self.aws.ypt.get_s3_file_content(
                                    referenceName=referenceName
                                    ,s3FullFolderPath=pt.users_path)
                                rslt = "ok**" + username + "ok**" + str(user_data["aws_certification_learning_path_tracker"]) + "ok**" + token
                                return rslt
                            else:
                                return str(resp).replace("of password","or password")
                        else:
                            return str(token).replace("of password","or password")
                    else:
                        return "User not confirmed yet."
                else:
                    return "User does not exist."
            else:
                return "User does not exist."
        else:
            return str(udat).replace("of password","or password")