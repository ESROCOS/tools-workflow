# H2020 ESROCOS Project
# Company: GMV Aerospace & Defence S.A.U.
# Licence: GPLv2

import sys
import os
import shutil
import subprocess
import stat

from mako.template import Template
from mako.runtime import Context

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

from . import ErrorCodes

def write_package_templates(templates, comp_name, project,dep,package_set_name, templ_dir, outdir):
    '''
    Write a set of Mako templates for a package.
    '''
    for t in templates:
        outfname = os.path.join(outdir, t.rstrip('.mako'))
        if not os.path.isfile(outfname):
            template = Template(filename=os.path.join(templ_dir, t))
            buf = StringIO()
            ctx = Context(buf, component_name=comp_name,project_name=project, dependencies=dep, package_set=package_set_name)
            template.render_context(ctx)
            f = open(outfname, 'w')
            f.write(buf.getvalue())
            f.close()
        else:
            print('File {} exists. Skipped.'.format(outfname))
    


def create_component(component_name, project_name, package_set_name, dependencies):
    '''
    Create a new package in autoproj environment.
    '''
    
    print('Creating the structure for a new package {}'.format(component_name))

    out_dir = os.getenv('AUTOPROJ_CURRENT_ROOT')
    out_dir = os.path.join(out_dir,component_name)
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    if not os.path.exists(os.path.join(out_dir, 'model')):
        os.makedirs(os.path.join(out_dir, 'model'))

    templ_dir = os.path.join(os.path.dirname(__file__), 'templates')
    templates = ['esrocos.yml.mako', 'manifest.xml.mako', 'CMakeLists.txt.mako', 'README.md.mako', os.path.join('model', 'CMakeLists.txt.mako')]


    write_package_templates(templates, component_name,project_name, dependencies,package_set_name, templ_dir, out_dir)

    files =['DataView.aadl', 'ConcurrencyView_Properties.aadl', 'DeploymentView.aadl', 'InterfaceView.aadl', 'Makefile', 'update_data_view.sh' ]

    for f in files:
        f_in = os.path.join(templ_dir,'model',f)
        f_out = os.path.join(out_dir, 'model',f)
        if not os.path.isfile(f_out):
            shutil.copyfile(f_in, os.path.join(out_dir, 'model',f))
            if f=="update_data_view.sh":
                st = os.stat(os.path.join(out_dir, 'model',f))
                os.chmod(os.path.join(out_dir, 'model',f),st.st_mode|stat.S_IEXEC)
        else:
            print('File {} exists. Skipped.'.format(f_out))

    if not os.path.exists(os.path.join(out_dir, 'model', 'work')):
        shutil.copytree(os.path.join(templ_dir, 'model','work'),os.path.join(out_dir, 'model','work'))
        




def check_dependency(dependency):
    '''
    Check if a dependency is defined in autoproj environment.
    '''
    dep_dir = os.getenv('AUTOPROJ_CURRENT_ROOT')
    dep_dir= os.path.join(dep_dir,dependency)

    if not os.path.exists(dep_dir):
        subprocess.run(["autoproj", "update", dependency])
        if not os.path.exists(dep_dir):
            print('This dependency does not exist')
            return False
        else:
            print('Updated and checked dependency {}\n'.format(dependency))
            return True
    else:
        print('Checked dependency {}\n'.format(dependency))
        return True
