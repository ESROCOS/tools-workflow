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


def create_component(component_name,project_name, package_set_name, dependencies):
    '''
    Create a new package in autoproj environment.
    '''
    'extract the default environmet'
    out_dir = os.getenv('AUTOPROJ_CURRENT_ROOT')
    out_dir = os.path.join(out_dir,component_name)
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    'first copy and customize the esrocos files'
    'insted of space-creator command, a copy of the space creator with modifications has being created to luch the taste-QT environmet as It was defined previously'
    lunch_qt = os.path.join( out_dir ,'esrocos_space-creator ' )
  
    templ_dir = os.path.join(os.path.dirname(__file__), 'templates')
    templates = ['esrocos.yml.mako', 'manifest.xml.mako', 'CMakeLists.txt.mako', 'README.md.mako']

    write_package_templates(templates, component_name,project_name, dependencies,package_set_name, templ_dir, out_dir)
    
    os.chdir(out_dir)
    os.system('esrocos_space-creator model')


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
