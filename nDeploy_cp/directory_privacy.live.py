#!/usr/bin/python
import os
import socket
import yaml
import cgi
import cgitb
try:
    import simplejson as json
except ImportError:
    import json


__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path


cgitb.enable()


def close_cpanel_liveapisock():
    """We close the cpanel LiveAPI socket here as we dont need those"""
    cp_socket = os.environ["CPANEL_CONNECT_SOCKET"]
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.connect(cp_socket)
    sock.sendall('<cpanelxml shutdown="1" />')
    sock.close()


close_cpanel_liveapisock()
form = cgi.FieldStorage()


print('Content-Type: text/html')
print('')
print('<html>')
print('<head>')
print('<title>XtendWeb</title>')
print(('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">'))
print(('<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js" crossorigin="anonymous"></script>'))
print(('<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script>'))
print(('<script src="js.js"></script>'))
print(('<link rel="stylesheet" href="styles.css">'))
print('</head>')
print('<body>')
print('<div id="main-container" class="container text-center">')
print('<div class="row">')
print('<div class="col-md-6 col-md-offset-3">')
print('<div class="logo">')
print('<a href="xtendweb.live.py" data-toggle="tooltip" data-placement="bottom" title="Start Over"><span class="glyphicon glyphicon-cog" aria-hidden="true"></span></a>')
print('<h4>XtendWeb</h4>')
print('</div>')
print('<ol class="breadcrumb">')
print('<li><a href="xtendweb.live.py"><span class="glyphicon glyphicon-home"></span></a></li>')
print('<li><a href="xtendweb.live.py">Set Domain</a></li><li class="active">Password Protected URLs</li>')
print('</ol>')
print('<div class="panel panel-default">')
if form.getvalue('domain'):
    # Get the domain name from form data
    mydomain = form.getvalue('domain')
    if mydomain.startswith('_wildcard_.'):
        cpmydomain = '*.'+mydomain.replace('_wildcard_.', '')
    else:
        cpmydomain = mydomain
    profileyaml = installation_path + "/domain-data/" + mydomain
    if os.path.isfile(profileyaml):
        # Get all config settings from the domains domain-data config file
        with open(profileyaml, 'r') as profileyaml_data_stream:
            yaml_parsed_profileyaml = yaml.safe_load(profileyaml_data_stream)
        protected_dir = yaml_parsed_profileyaml.get('protected_dir', None)
        cpaneluser = os.environ["USER"]
        cpdomainjson = "/var/cpanel/userdata/" + cpaneluser + "/" + cpmydomain + ".cache"
        with open(cpdomainjson, 'r') as cpaneldomain_data_stream:
            json_parsed_cpaneldomain = json.load(cpaneldomain_data_stream)
        document_root = json_parsed_cpaneldomain.get('documentroot')
        print(('<div class="panel-heading"><h3 class="panel-title">Domain: <strong>'+mydomain+'</strong></h3></div><div class="panel-body">'))
        print('<div class="alert alert-info">')
        print('<ul class="list text-left">')
        print('<li>Password protection works along with cPanel - "Directory Privacy" feature</li>')
        print('<li>Please setup a password for the folder in cPanel <span class="glyphicon glyphicon-chevron-right" aria-hidden="true"></span> FILES <span class="glyphicon glyphicon-chevron-right" aria-hidden="true"></span> Directory Privacy</li>')
        print('<li>The path entered below must begin with <kbd>/</kbd><br>examples are <kbd>/</kbd> <kbd>/blog</kbd> <kbd>/blog/dev</kbd> etc.</li>')
        print('</ul>')
        print('</div>')
        print('<div class="desc">')
        print('<p>Enter a password protected URL below:</p>')
        print('<form class="form-inline" action="save_directory_privacy.live.py">')
        print('<div class="form-group">')
        print('<div class="input-group">')
        print('<span class="input-group-addon">')
        print(document_root)
        print('</span>')
        print('<input class="form-control" placeholder="/blog" type="text" name="protectedurl">')
        print(('<input class="hidden" name="domain" value="'+mydomain+'">'))
        print(('<input class="hidden" name="action" value="add">'))
        print('<span class="input-group-btn">')
        print('<input class="btn btn-primary" type="submit" value="Add">')
        print('</span>')
        print('</div>')
        print('</div>')
        print('</form>')
        print('</div>')
        if protected_dir:
            print(('<p>Current password protected URLs:</p>'))
            print('<ul class="list-group">')
            for theurl in protected_dir:
                print('<li class="list-group-item">')
                print('<form class="form-inline" action="save_directory_privacy.live.py">')
                print('<div class="form-group"><kbd>')
                print(document_root+theurl)
                print('</kbd></div>')
                print('<span class="glyphicon glyphicon-option-vertical" aria-hidden="true"></span>')
                print('<div class="form-group"><input class="btn btn-xs btn-danger" type="submit" value="REMOVE">')
                print(('<input class="hidden" name="domain" value="'+mydomain+'">'))
                print(('<input class="hidden" name="action" value="del"></div>'))
                print(('<input class="hidden" name="protectedurl" value="'+theurl+'">'))
                print('</form>')
                print('</li>')
            print('</ul>')
    else:
        print('<div class="alert alert-danger"><span class="glyphicon glyphicon-alert" aria-hidden="true"></span> ERROR: domain-data file i/o error</div>')
else:
    print('<div class="alert alert-danger"><span class="glyphicon glyphicon-alert" aria-hidden="true"></span> ERROR: Forbidden</div>')
print('</div>')
print('<div class="panel-footer"><small>Powered by <a target="_blank" href="http://xtendweb.gnusys.net/">XtendWeb</a> <span class="glyphicon glyphicon-flash" aria-hidden="true"></span> Themed by <a target="_blank" href="http://www.stirstudiosdesign.com/">StirStudios</a></small></div>')
print('</div>')
print('<div class="help pull-right"><a target="_blank" href="http://xtendweb.gnusys.net/"><span class="glyphicon glyphicon-question-sign" aria-hidden="true"></span> <em>Need Help?</em></a></div>')
print('</div>')
print('</div>')
print('</div>')
print('</body>')
print('</html>')