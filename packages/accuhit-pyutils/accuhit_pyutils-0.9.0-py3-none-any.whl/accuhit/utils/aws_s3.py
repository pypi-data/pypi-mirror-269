# -*- coding: utf-8 -*-
import logging
import traceback
import boto3
import botocore.exceptions
import re

logger = logging.getLogger(__name__)

SERVICE_NAME = "s3"


class S3Config(object):
    region = None
    bucket_name = None
    access_key = None
    secret_key = None

    def __init__(self, bucket_name, access_key, secret_key, region=None):
        self.bucket_name = bucket_name
        self.access_key = access_key
        self.secret_key = secret_key
        self.region = region


def download_file(s3_config, source_file, target_file):
    assert s3_config is not None
    try:
        s3 = boto3.resource(SERVICE_NAME,
                            region_name=s3_config.region,
                            aws_access_key_id=s3_config.access_key,
                            aws_secret_access_key=s3_config.secret_key)

        mlbucket = s3.Bucket(s3_config.bucket_name)
        mlbucket.download_file(source_file, target_file)

    except botocore.exceptions.ClientError as ce:
        if ce.response['Error']['Code'] == "404":
            logger.error("download s3 file not found, file is {}".format(source_file))
        else:
            raise


def download_files(s3_config, s3_path, target_path, filter_name=None):
    assert s3_config and s3_path
    try:
        s3 = boto3.resource(SERVICE_NAME,
                            region_name=s3_config.region,
                            aws_access_key_id=s3_config.access_key,
                            aws_secret_access_key=s3_config.secret_key)

        mlbucket = s3.Bucket(s3_config.bucket_name)

        # prefix = re.compile("^\/").sub("", s3_path)
        prefix = s3_path[1:] if s3_path.startswith("/") else s3_path
        flist = []
        for file_obj in mlbucket.objects.filter(Prefix=prefix):
            # fkey = file_obj.key
            if filter_name and filter_name not in file_obj.key:
                continue
            fkey = file_obj.key
            fname = fkey.replace(prefix, "")
            fname = fname[fname.rfind("/") + 1:]
            if len(fname) == 0:
                logger.info("skip the remote file({})...".format(fkey))
                continue
            fname = "{}/{}".format(target_path, fname)
            # logger.info("download s3 file({}) to {}".format(fkey, fname))
            mlbucket.download_file(fkey, fname)
            flist.append(fname)
        logger.info("download from remote completed, total is {}".format(len(flist)))
        return flist

    except botocore.exceptions.ClientError as ce:
        if ce.response['Error']['Code'] == "404":
            logger.error("remote file not found, path is {}".format(s3_path))
        else:
            raise


def get_file_list(s3_config, s3_path, filter_name=None):
    assert s3_config and s3_path
    try:
        s3 = boto3.resource(SERVICE_NAME,
                            region_name=s3_config.region,
                            aws_access_key_id=s3_config.access_key,
                            aws_secret_access_key=s3_config.secret_key)

        mlbucket = s3.Bucket(s3_config.bucket_name)
        # prefix = re.compile("^\/").sub("", source_path)
        prefix = s3_path[1:] if s3_path.startswith("/") else s3_path
        # flist = [files.key for files in mlbucket.objects.filter(Prefix=prefix)]
        flist = []
        for file_obj in mlbucket.objects.filter(Prefix=prefix):
            # fkey = file_obj.key
            # fname = fkey.replace(prefix, "")
            # fname = fname[fname.rfind("/") + 1:]
            if filter_name and filter_name not in file_obj.key:
                continue
            flist.append(file_obj.key)
        return flist
    except:
        logger.error(traceback.format_exc())
    return None


def upload_file(s3_config, source_file, target_file):
    """

    :param s3_config:
    :param source_file: 完整路徑+檔案名稱
    :param target_file: 完整路徑+檔案名稱
    :return:
    """
    try:
        s3 = boto3.resource(SERVICE_NAME,
                            region_name=s3_config.region,
                            aws_access_key_id=s3_config.access_key,
                            aws_secret_access_key=s3_config.secret_key)

        mlbucket = s3.Bucket(s3_config.bucket_name)
        mlbucket.upload_file(source_file, target_file)
        logger.info("upload {} to S3({}) success!".format(source_file, target_file))
    except:
        logger.error(traceback.format_exc())
        logger.info("upload {} to S3({}) has error...".format(source_file, target_file))
