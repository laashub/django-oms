# -*- coding: utf-8 -*-
# author: itimor

from rest_framework import serializers
from jobs.models import Jobs, DeployJobs, Deploycmd
from hosts.models import Host
from users.models import User
from omsBackend.settings import sapi


class JobsSerializer(serializers.ModelSerializer):
    deploy_hosts = serializers.SlugRelatedField(many=True, queryset=Host.objects.all(), slug_field='hostname')

    class Meta:
        model = Jobs
        fields = ['url', 'id', 'name', 'code_repo', 'code_url', 'deploy_hosts', 'deploy_path', 'create_time', 'showdev',
                  'desc']


# class DeployenvSerializer(serializers.ModelSerializer):
#     job = serializers.SlugRelatedField(queryset=Jobs.objects.all(), slug_field='name')
#     hosts = serializers.SlugRelatedField(many=True, queryset=Host.objects.all(), slug_field='hostname')
#
#     class Meta:
#         model = Deployenv
#         fields = ['url', 'id', 'job', 'name', 'path', 'hosts', 'desc']


class DeployJobsSerializer(serializers.ModelSerializer):
    job = serializers.SlugRelatedField(queryset=Jobs.objects.all(), slug_field='name')
    action_user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')

    class Meta:
        model = DeployJobs
        fields = ['url', 'id', 'job', 'j_id', 'deploy_status', 'deploy_hosts', 'version', 'content', 'deploy_cmd',
                  'action_user', 'result', 'create_time']

    def create(self, validated_data):
        deploy_cmd = validated_data["deploy_cmd"]
        deploy_hosts = validated_data["deploy_hosts"]
        printcmd = "echo '发布主机：'%s; echo '发布命令：'%s" % (deploy_hosts, deploy_cmd)
        jid = sapi.remote_cmd(tgt=deploy_hosts.split(','), fun='cmd.run', arg=deploy_cmd)
        validated_data["j_id"] = jid
        deployjob = DeployJobs.objects.create(**validated_data)
        deployjob.save()
        return deployjob


class DeploycmdSerializer(serializers.ModelSerializer):
    job = serializers.SlugRelatedField(queryset=Jobs.objects.all(), slug_field='name')

    class Meta:
        model = Deploycmd
        fields = ['url', 'id', 'job', 'name', 'deploy_cmd']
