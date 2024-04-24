import configparser
import json
import math
import os
import time

import boto3
from botocore.exceptions import NoCredentialsError

import pandas as pd
import requests

import gzip
import shutil
import re

from nemo_library.symbols import (
    ENDPOINT_URL_PROJECTS_FILE_RE_UPLOAD_ABORT,
    ENDPOINT_URL_PROJECTS_FILE_RE_UPLOAD_FINALIZE,
    ENDPOINT_URL_PROJECTS_FILE_RE_UPLOAD_INITIALIZE,
    ENDPOINT_URL_PROJECTS_FILE_RE_UPLOAD_KEEP_ALIVE,
    ENDPOINT_URL_PERSISTENCE_PROJECT_PROPERTIES,
    ENDPOINT_URL_PROJECTS_ALL,
    ENDPOINT_URL_PERSISTENCE_METADATA_IMPORTED_COLUMNS,
    ENDPOINT_URL_PERSISTENCE_METADATA_SET_COLUMN_PROPERTIES,
    ENDPOINT_URL_PERSISTENCE_METADATA_CREATE_IMPORTED_COLUMN,
    ENDPOINT_URL_PERSISTENCE_METADATA_DELETE_IMPORTED_COLUMN,
    ENDPOINT_URL_REPORT_EXPORT,
    ENDPOINT_URL_QUEUE_INGEST_DATA_V2,
    ENDPOINT_URL_QUEUE_TASK_RUNS,
    ENDPOINT_URL_TVM_S3_ACCESS,
    FILE_UPLOAD_CHUNK_SIZE,
    RESERVED_KEYWORDS
)

NEMO_URL = "https://enter.nemo-ai.com"
DEFAULT_PROJECT_NAME = "ERP Business Processes"


class NemoLibrary:
    #################################################################################################################################################################

    def __init__(self):
        config = configparser.ConfigParser()
        config.read("config.ini")
        self._tenant_ = config["nemo_library"]["tenant"]
        self._environment_ = config["nemo_library"]["environment"]
        self._userid_ = config["nemo_library"]["userid"]
        self._password_ = config["nemo_library"]["password"]
        self._nemo_url_ = config["nemo_library"]["nemo_url"]

        match self._environment_:
            case "demo":
                self._cognito_url_ = "https://cognito-idp.eu-central-1.amazonaws.com/eu-central-1_1ZbUITj21"
                self._cognito_appclientid = "7tvfugcnunac7id3ebgns6n66u"
                self._cognito_authflow_ = "USER_PASSWORD_AUTH"
            case "dev":
                self._cognito_url_ = "https://cognito-idp.eu-central-1.amazonaws.com/eu-central-1_778axETqE"
                self._cognito_appclientid = "4lr89aas81m844o0admv3pfcrp"
                self._cognito_authflow_ = "USER_PASSWORD_AUTH"
            case "prod":
                self._cognito_url_ = "https://cognito-idp.eu-central-1.amazonaws.com/eu-central-1_1oayObkcF"
                self._cognito_appclientid = "8t32vcmmdvmva4qvb79gpfhdn"
                self._cognito_authflow_ = "USER_PASSWORD_AUTH"
            case "challenge":
                self._cognito_url_ = "https://cognito-idp.eu-central-1.amazonaws.com/eu-central-1_U2V9y0lzx"
                self._cognito_appclientid = "43lq8ej98uuo8hvnoi1g880onp"
                self._cognito_authflow_ = "USER_PASSWORD_AUTH"
            case _:
                raise Exception(f"unknown environment '{self._environment_}' provided")

        super().__init__()

    #################################################################################################################################################################

    def _login(self):
        headers = {
            "X-Amz-Target": "AWSCognitoIdentityProviderService.InitiateAuth",
            "Content-Type": "application/x-amz-json-1.1",
        }

        authparams = {"USERNAME": self._userid_, "PASSWORD": self._password_}

        data = {
            "AuthParameters": authparams,
            "AuthFlow": self._cognito_authflow_,
            "ClientId": self._cognito_appclientid,
        }

        # login and get tokenb

        response_auth = requests.post(
            self._cognito_url_, headers=headers, data=json.dumps(data)
        )
        if response_auth.status_code != 200:
            raise Exception(
                f"request failed. Status: {response_auth.status_code}, error: {response_auth.text}"
            )
        tokens = json.loads(response_auth.text)
        id_token = tokens["AuthenticationResult"]["IdToken"]
        access_token = tokens["AuthenticationResult"]["AccessToken"]
        refresh_token = tokens["AuthenticationResult"].get(
            "RefreshToken"
        )  # Some flows might not return a RefreshToken

        return id_token, access_token, refresh_token

    #################################################################################################################################################################

    def _headers(self):
        tokens = self._login()

        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {tokens[0]}",
            "refresh-token": tokens[2],
            "api-version": "1.0",
        }
        return headers

    #################################################################################################################################################################

    def _get_file_size_in_characters_(self, file_path):
        character_count = 0
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                character_count += len(line)
        return character_count

    #################################################################################################################################################################

    def _split_file_(self, file_path, chunk_size):
        with open(file_path, "r", encoding="utf-8") as file:
            while True:
                data = file.read(chunk_size)
                if not data:
                    break
                yield data

    #################################################################################################################################################################

    def getProjectList(self):
        headers = self._headers()

        response = requests.get(
            self._nemo_url_ + ENDPOINT_URL_PROJECTS_ALL, headers=headers
        )
        if response.status_code != 200:
            raise Exception(
                f"request failed. Status: {response.status_code}, error: {response.text}"
            )
        resultjs = json.loads(response.text)
        df = pd.json_normalize(resultjs)
        return df

    #################################################################################################################################################################

    def getProjectID(self, projectname: str):
        if projectname == None:
            projectname = DEFAULT_PROJECT_NAME
        df = self.getProjectList()
        crmproject = df[df["displayName"] == projectname]
        if len(crmproject) != 1:
            raise Exception(f"could not identify project name {projectname}")
        project_id = crmproject["id"].to_list()[0]
        return project_id

    #################################################################################################################################################################

    def getImportedColumns(self, projectname: str):
        project_id = None

        try:
            project_id = self.getProjectID(projectname)

            # initialize reqeust
            headers = self._headers()
            response = requests.get(
                self._nemo_url_
                + ENDPOINT_URL_PERSISTENCE_METADATA_IMPORTED_COLUMNS.format(
                    projectId=project_id
                ),
                headers=headers,
            )
            if response.status_code != 200:
                raise Exception(
                    f"request failed. Status: {response.status_code}, error: {response.text}"
                )
            resultjs = json.loads(response.text)
            df = pd.json_normalize(resultjs)
            return df

        except Exception as e:
            if project_id == None:
                raise Exception("process stopped, no project_id available")
            raise Exception("process aborted")

    #################################################################################################################################################################

    def int_to_base62(self, n):
        chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
        if n == 0:
            return "0"
        arr = []
        while n:
            n, rem = divmod(n, 62)
            arr.append(chars[rem])
        arr.reverse()
        if len(arr) > 1 and arr[0] == "1":
            arr[0] = "z"
        return "".join(arr)

    def setMetadataSortOrder(self, projectname: str, fields: list):
        try:
            # everything is case sensitive, thus we convert everything to lower case for a better mapping
            fields_lower = [field.lower() for field in fields]

            # store position in fields list
            field_order = {field: index for index, field in enumerate(fields_lower)}

            # get columns and apply new sort order
            df_imported = self.getImportedColumns(projectname=projectname)
            print(df_imported)
            df_imported["focusOrder"] = (
                df_imported["displayName"].str.lower().map(field_order)
            )

            # apply base62-coded sort order
            df_imported["focusOrder"] = df_imported["focusOrder"].apply(
                lambda x: self.int_to_base62(x) if not pd.isna(x) else x
            )

            # initialize reqeust
            headers = self._headers()

            for idx, row in df_imported.iterrows():
                print(idx, row["internalName"])
                response = requests.put(
                    self._nemo_url_
                    + ENDPOINT_URL_PERSISTENCE_METADATA_SET_COLUMN_PROPERTIES.format(
                        id=row["id"]
                    ),
                    headers=headers,
                    json=row.to_dict(),
                )
                if response.status_code != 200:
                    raise Exception(
                        f"request failed. Status: {response.status_code}, error: {response.text}"
                    )

        except Exception as e:
            raise Exception("setMetadataSortOrder metadata aborted")

    #################################################################################################################################################################

    def copyMetadata(self, projectname_src, projectname_tgt):
        try:
            # load columns from both projects
            df_src = self.getImportedColumns(projectname_src)
            df_tgt = self.getImportedColumns(projectname_tgt)

            # make code bullet proof (we don not support everything yet)
            if len(df_src) != len(df_tgt):
                raise Exception(
                    "Target dataset has different length ({len_tgt}) than source ({len_src})".format(
                        len_tgt=len(df_tgt), len_src=len(df_src)
                    )
                )

            # check for different values in relevant fields

            # merge datasets on "internalName"
            merged_df = pd.merge(
                df_src, df_tgt, on="internalName", suffixes=("_src", "_tgt")
            )

            # check whether the result still has the same number of records
            if len(df_src) != len(df_tgt):
                raise Exception(
                    "Merge dataset has different length ({len_mrg}) than source ({len_src})".format(
                        len_mrg=len(merged_df), len_src=len(df_src)
                    )
                )

            # filter on differences now
            columns_to_compare = [
                "dataType",
                "description",
                # "attributeGroupInternalName",
                # "groupByColumnInternalName",
                # "order",
                # "focusOrder",
            ]
            conditions = (
                merged_df[col + "_src"] != merged_df[col + "_tgt"]
                for col in columns_to_compare
            )
            combined_condition = pd.concat(conditions, axis=1).any(axis=1)
            diff_df = merged_df[combined_condition]

            # create results dataset with differences
            output_columns = [
                "id_src",
                "id_tgt",
                "internalName",
            ] + [
                col + suffix
                for col in columns_to_compare
                for suffix in ["_src", "_tgt"]
            ]
            result_df = diff_df[output_columns]

            print(result_df)

        except Exception as e:
            raise Exception("copy metadata aborted")

    #################################################################################################################################################################

    def ReUploadFile(self, projectname: str, filename: str):
        project_id = None
        headers = None
        upload_id = None

        try:
            project_id = self.getProjectID(projectname)

            headers = self._headers()

            print(
                f"upload of file '{filename}' into project '{projectname}' initiated..."
            )

            ####
            # start upload process

            # we need to upload file in chunks. Default is 6MB size chunks

            # usually we would get the file size with os.path.getsize(filename) - but this is
            # the size in Bytes, not in (UTF-8)-characters. So we have to calculate the size
            # by our own

            file_size = self._get_file_size_in_characters_(filename)
            total_chunks = math.ceil(file_size / FILE_UPLOAD_CHUNK_SIZE)

            print(f"file size: {file_size:,}")
            print(f"chunk size: {FILE_UPLOAD_CHUNK_SIZE:,}")
            print(f"--> total chunks: {total_chunks:,}")
            data = {"projectId": project_id, "partCount": total_chunks}

            # initialize upload
            response = requests.post(
                self._nemo_url_ + ENDPOINT_URL_PROJECTS_FILE_RE_UPLOAD_INITIALIZE,
                headers=headers,
                json=data,
            )
            if response.status_code != 200:
                raise Exception(
                    f"request failed. Status: {response.status_code}, error: {response.text}"
                )
            resultjs = json.loads(response.text)
            df = pd.json_normalize(resultjs)
            upload_id = resultjs["uploadId"]
            upload_urls = resultjs["urls"]
            partETags = pd.DataFrame({"partNumber": [None], "eTag": [None]})

            file_chunks = self._split_file_(filename, FILE_UPLOAD_CHUNK_SIZE)

            for index, url in enumerate(upload_urls, start=1):
                # post keep alive message

                karesponse = requests.post(
                    url=self._nemo_url_
                    + ENDPOINT_URL_PROJECTS_FILE_RE_UPLOAD_KEEP_ALIVE.format(
                        projectId=project_id, uploadId=upload_id
                    ),
                    headers=headers,
                )
                if (
                    karesponse.status_code != 204
                ):  # this is the defined response that we expect, not 200
                    raise Exception(
                        f"request failed. Status: {karesponse.status_code}, error: {karesponse.text}"
                    )

                print(f"upload part {index}")
                headers_upload = {
                    "Content-Type": "text/csv",
                }
                data = next(file_chunks, None)

                response = requests.put(
                    url=url,
                    headers=headers_upload,
                    data=data.encode("utf-8"),
                )
                if response.status_code != 200:
                    raise Exception(
                        f"request failed. Status: {response.status_code}, error: {response.text}"
                    )

                partETags.at[index - 1, "partNumber"] = index
                partETags.at[index - 1, "eTag"] = response.headers["ETag"].strip('"')

            print("finalize upload")

            data = {
                "uploadId": upload_id,
                "projectId": project_id,
                "fieldDelimiter": ";",
                "recordDelimiter": "\n",
                "partETags": partETags.to_dict(orient="records"),
            }
            datajs = json.dumps(data, indent=2)
            response = requests.post(
                self._nemo_url_ + ENDPOINT_URL_PROJECTS_FILE_RE_UPLOAD_FINALIZE,
                headers=headers,
                data=datajs,
            )
            if response.status_code != 204:
                raise Exception(
                    f"request failed. Status: {response.status_code}, error: {response.text}"
                )

            print("upload finished")

        except Exception as e:
            if project_id == None:
                raise Exception("upload stopped, no project_id available")

            if upload_id == None:
                raise Exception("upload stopped, no upload_id available")

            # we are sure that all information to anbandon the upload are available, we do so now

            data = {"uploadId": upload_id, "projectId": project_id}
            response = requests.post(
                self._nemo_url_ + ENDPOINT_URL_PROJECTS_FILE_RE_UPLOAD_ABORT,
                headers=headers,
                json=data,
            )
            if response.status_code != 204:
                raise Exception(
                    f"request failed. Status: {response.status_code}, error: {response.text}"
                )

            raise Exception("upload aborted")

    #################################################################################################################################################################

    def ReUploadFileIngestionV2(self, projectname: str, filename: str):
        project_id = None
        headers = None

        try:
            project_id = self.getProjectID(projectname)

            headers = self._headers()

            print(
                f"upload of file '{filename}' into project '{projectname}' initiated..."
            )

            # Zip the file before uploading
            gzipped_filename = filename + '.gz'
            with open(filename, 'rb') as f_in:
                with gzip.open(gzipped_filename, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            print(f"File {filename} has been compressed to {gzipped_filename}")

            ####
            # start upload process

            # Retrieve temp. Creds. from NEMO TVM

            response = requests.get(
                self._nemo_url_ + ENDPOINT_URL_TVM_S3_ACCESS,
                headers=headers,
                )

            if response.status_code != 200:
                raise Exception(
                    f"request failed. Status: {response.status_code}, error: {response.text}"
                )
            
            aws_credentials = json.loads(response.text)

            aws_access_key_id = aws_credentials['accessKeyId']
            aws_secret_access_key = aws_credentials['secretAccessKey']
            aws_session_token = aws_credentials['sessionToken']

            # Create an S3 client
            s3 = boto3.client(
                "s3",
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
                aws_session_token=aws_session_token,
            )

            try:
                # Upload the file
                s3filename = self._tenant_ + "/ingestv2/" + os.path.basename(gzipped_filename)
                s3.upload_file(
                    gzipped_filename,
                    "nemoinfrastructurestack-nemouploadbucketa98fe899-1s2ocvunlg3vs",
                    s3filename,
                )
                print(f"File {filename} uploaded successfully to s3 ({s3filename})")
            except FileNotFoundError:
                print(f"The file {filename} was not found.")
            except NoCredentialsError:
                print("Credentials not available or incorrect.")

            # file is uploaded, ingest it now into project
            data = {
                "project_id": project_id,
                "s3_filepath": f"s3://nemoinfrastructurestack-nemouploadbucketa98fe899-1s2ocvunlg3vs/{s3filename}",
            }
            response = requests.post(
                self._nemo_url_ + ENDPOINT_URL_QUEUE_INGEST_DATA_V2,
                headers=headers,
                json=data,
            )
            if response.status_code != 200:
                raise Exception(
                    f"request failed. Status: {response.status_code}, error: {response.text}"
                )
            print("ingestion successful")

            # wait for task to be completed
            taskid = response.text.replace("\"","")
            while True:
                data = {
                    "sort_by" : "submit_at",
                    "is_sort_ascending" : "False",
                    "page" : 1,
                    "page_size" : 20
                }
                response = requests.get(
                    self._nemo_url_ + ENDPOINT_URL_QUEUE_TASK_RUNS,
                    headers=headers,
                    json=data,
                )
                resultjs = json.loads(response.text)
                df = pd.json_normalize(resultjs["records"])
                df_filtered = df[df["id"]==taskid]
                if len(df_filtered) != 1:
                    raise Exception(
                        f"data ingestions request failed, task id that have been provided not found in tasks list"
                    )
                status = df_filtered["status"].iloc[0]
                print("Status: ",status)
                if status == "failed":
                    raise Exception(
                        f"data ingestion request faild, task id return status FAILED"
                    )
                if status == "finished":
                    records = df_filtered["records"].iloc[0]
                    print(f"Ingestion finished. {records} records loaded")
                    break
                time.sleep(1)
                                            
        except Exception as e:
            if project_id == None:
                raise Exception("upload stopped, no project_id available")

            raise Exception("upload aborted")

    #################################################################################################################################################################

    def LoadReport(self, projectname: str, report_guid: str, max_pages=None):
        project_id = self.getProjectID(projectname)

        print(f"Loading report: {report_guid} from project {projectname}")

        headers = self._headers()

        # INIT REPORT PAYLOAD (REQUEST BODY)
        report_params = {"id": report_guid, "project_id": project_id}

        response_report = requests.post(
            self._nemo_url_ + ENDPOINT_URL_REPORT_EXPORT,
            headers=headers,
            json=report_params,
        )

        if response_report.status_code != 200:
            raise Exception(
                f"request failed. Status: {response_report.status_code}, error: {response_report.text}"
            )

        # extract download URL from response
        csv_url = response_report.text.strip('"')
        print(f"Downloading CSV from: {csv_url}")

        # download the file into pandas
        try:
            result = pd.read_csv(csv_url)
            if "_RECORD_COUNT" in result.columns:
                result.drop(columns=["_RECORD_COUNT"],inplace=True)
        except Exception as e:
            raise Exception(
                f"download failed. Status: {e}"
            )
        return result

    #################################################################################################################################################################

    def ProjectProperty(self, projectname:str, propertyname:str):
        headers = self._headers()
        project_id = self.getProjectID(projectname)

        ENDPOINT_URL = (
            self._nemo_url_
            + ENDPOINT_URL_PERSISTENCE_PROJECT_PROPERTIES.format(projectId=project_id,request=propertyname)
        )

        response = requests.get(ENDPOINT_URL, headers=headers)

        if response.status_code != 200:
            raise Exception(
                f"request failed. Status: {response.status_code}, error: {response.text}"
            )

        return response.text

    #################################################################################################################################################################

    def synchronizeCsvColsAndImportedColumns(self, projectname:str, filename:str):
        importedColumns = self.getImportedColumns(projectname)
        project_id = self.getProjectID(projectname)

        # Read the first line of the CSV file to get column names
        with open(filename, 'r') as file:
            first_line = file.readline().strip()

        # Split the first line into a list of column names
        csv_column_names = first_line.split(';')

        # Check if a record exists in the DataFrame for each column
        for column_name in csv_column_names:
            displayName = column_name
            column_name = self.clean_column_name(column_name, RESERVED_KEYWORDS)  # Assuming you have the clean_column_name function from the previous script

            # Check if the record with internal_name equal to the column name exists
            if not importedColumns[importedColumns['internalName'] == column_name].empty:
                print(f"Record found for column '{column_name}' in the DataFrame.")
            else:
                print(f"******************************No record found for column '{column_name}' in the DataFrame.")
                new_importedColumn = {
                    "id":"",
                    "internalName":column_name,
                    "displayName":displayName,
                    "importName":displayName,
                    "description":"",
                    "dataType":"string",
                    "categorialType": False,
                    "businessEvent": False,
                    "unit": "",
                    "columnType": "ExportedColumn",
                    "tenant": self._tenant_,
                    "projectId": project_id,
                }

                self.createImportedColumn(new_importedColumn, project_id)

    #################################################################################################################################################################

    def clean_column_name(self, column_name, reserved_keywords):
        # If csv column name is empty, return "undefined_name"
        if not column_name:
            return "undefined_name"

        # Replace all chars not matching regex [^a-zA-Z0-9_] with empty char
        cleaned_name = re.sub(r'[^a-zA-Z0-9_]', '', column_name)

        # Convert to lowercase
        cleaned_name = cleaned_name.lower()

        # If starts with a number, concatenate "numeric_" to the beginning
        if cleaned_name[0].isdigit():
            cleaned_name = "numeric_" + cleaned_name

        # Replace all double "_" chars with one "_"
        cleaned_name = re.sub(r'_{2,}', '_', cleaned_name)

        # If length of csv column name equals 1 or is a reserved keyword, concatenate "_" to the end
        if len(cleaned_name) == 1 or cleaned_name in reserved_keywords:
            cleaned_name += "_"

        return cleaned_name
    
    #################################################################################################################################################################

    def createImportedColumn(self, importedColumn:json, project_id:str):
        try:

            # initialize reqeust
            headers = self._headers()
            response = requests.post(
                self._nemo_url_
                + ENDPOINT_URL_PERSISTENCE_METADATA_CREATE_IMPORTED_COLUMN,
                headers=headers,
                json=importedColumn
            )
            if response.status_code != 201:
                raise Exception(
                    f"request failed. Status: {response.status_code}, error: {response.text}"
                )
            resultjs = json.loads(response.text)
            df = pd.json_normalize(resultjs)
            return df

        except Exception as e:
            raise Exception("process aborted")