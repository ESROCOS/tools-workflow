COMPONENT_NAME: ${component_name}
PROJECT_NAME: ${project_name}
deps:
%for d in dependencies:
- ${d}
%endfor
