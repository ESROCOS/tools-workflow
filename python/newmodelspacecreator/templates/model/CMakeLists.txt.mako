# H2020 ESROCOS Project
# Company: GMV Aerospace & Defence S.A.U.
# Licence: GPLv2

# Name of the reusable TASTE component
set(COMPONENT_NAME ${project_name})


# Preinstall ASN.1 types, headers and libraries for first build
#file(GLOB ASN1 ${"${CMAKE_SOURCE_DIR}"}/asn/*.asn)
#esrocos_preinstall_files(pus_asn1_${"${COMPONENT_NAME}"} types/${project_name}/ ${"${ASN1}"})

#if exists include 
#file(GLOB HEADERS ${"${CMAKE_SOURCE_DIR}"}/include/*.h)
#esrocos_preinstall_files(pus_headers_${"${COMPONENT_NAME}"} include/${project_name} ${"${HEADERS}"})


esrocos_build_taste(${"${COMPONENT_NAME}"}
    SOURCES
    hello_world
    BINARIES
    work/binaries/x86_partition
#    DEPENDS
#    dependencies
)



