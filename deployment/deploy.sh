#!/bin/bash


BASE_DIR=`pwd`

GIT_PROJECT_BASE='https://github.com/gn01842919'




# my_focus_news (Django)
WEB_PROJECT="my_focus_news"
WEB_DIR="${BASE_DIR}/${WEB_PROJECT}"
DJANGO_CONFIG="${WEB_DIR}/${WEB_PROJECT}/settings.py"
BACKUP_DJANGO_CONFIG="django-settings.backup"

# news_scraper
SCRAPER_PROJECT="news_scraper"
SCRAPER_DIR="${BASE_DIR}/${SCRAPER_PROJECT}"
SCRAPER_CONFIG="${SCRAPER_DIR}/settings.py"
BACKUP_SCRAPER_CONFIG="scraper-settings.backup"

# db_operation_api
DB_API_PROJECT="db_operation_api"
DB_API_DIR="${SCRAPER_DIR}/${DB_API_PROJECT}"

# backup
CONF_BACKUP_DIR="${WEB_DIR}/deployment/.deploy_backup"

# docker
DOCKER_COMPOSE_DIR="${WEB_DIR}/deployment/docker"
DOCKER_COMPOSE_CONFIG="${DOCKER_COMPOSE_DIR}/docker-compose.yml"
BACKUP_DOCKER_COMPOSE_CONFIG="docker-compose.yml.backup"
DOCKERFILE_FOLDER="${DOCKER_COMPOSE_DIR}/my-python-env"


clone_or_update_project_sources(){
    clone_or_pull_a_project "${WEB_PROJECT}" "${WEB_DIR}"
    clone_or_pull_a_project "${SCRAPER_PROJECT}" "${SCRAPER_DIR}"
    clone_or_pull_a_project "${DB_API_PROJECT}" "${DB_API_DIR}"
}

clone_or_pull_a_project(){
    # $1: project_name
    local project_name="$1"
    local source_dir="$2"

    if [ ! -d ${source_dir} ]; then
        echo "[+] git clone: ${project_name}.git"
        git clone "${GIT_PROJECT_BASE}/${project_name}.git" "${source_dir}"
    else
        cd ${source_dir}
        echo "[+] git pull: `pwd`"
        cd ${BASE_DIR}
    fi
}

backup_all_configs(){
    [ -d "${CONF_BACKUP_DIR}" ] || mkdir -p "${CONF_BACKUP_DIR}"
    backup_config "${DJANGO_CONFIG}" "${BACKUP_DJANGO_CONFIG}"
    backup_config "${SCRAPER_CONFIG}" "${BACKUP_SCRAPER_CONFIG}"
    backup_config "${DOCKER_COMPOSE_CONFIG}" "${BACKUP_DOCKER_COMPOSE_CONFIG}"
}

restore_all_configs(){
    restore_config "${DJANGO_CONFIG}" "${BACKUP_DJANGO_CONFIG}"
    restore_config "${SCRAPER_CONFIG}" "${BACKUP_SCRAPER_CONFIG}"
    restore_config "${DOCKER_COMPOSE_CONFIG}" "${BACKUP_DOCKER_COMPOSE_CONFIG}"
}

backup_config(){
    CONFIG_FILE=$1
    BACKUP_FILE="${CONF_BACKUP_DIR}/$2"
    [ -f "${BACKUP_FILE}" ] || cp "${CONFIG_FILE}" "${BACKUP_FILE}"
}

restore_config(){
    CONFIG_FILE=$1
    BACKUP_FILE="${CONF_BACKUP_DIR}/$2"
    [ -f "${BACKUP_FILE}" ] && cp "${BACKUP_FILE}" "${CONFIG_FILE}"
}

copy_pip_requirements_for_building_images(){
    local filename="requirements.txt"
    cp "${WEB_DIR}/deployment/${filename}" "${DOCKERFILE_FOLDER}/${WEB_PROJECT}-${filename}"
    cp "${SCRAPER_DIR}/${filename}" "${DOCKERFILE_FOLDER}/${SCRAPER_PROJECT}-${filename}"
}

modify_django_config(){
    # $1: Hostname or ip for 'ALLOWED_HOSTS'
    # $2: password of the database
    local pattern_allow_hosts='^ALLOWED_HOSTS = .*'
    local allow_hosts_setting="ALLOWED_HOSTS = ['$1']"
    sed -i "s/${pattern_allow_hosts}/${allow_hosts_setting}/g" ${DJANGO_CONFIG}

    local pattern_debug='^DEBUG = .*'
    local debug_setting="DEBUG = False"
    sed -i "s/${pattern_debug}/${debug_setting}/g" ${DJANGO_CONFIG}

    if [ -n "$2" ];then
        local pattern_db_password="'PASSWORD': .*,$"
        local db_password_setting="'PASSWORD': '$2',"
        sed -i "s/${pattern_db_password}/${db_password_setting}/g" ${DJANGO_CONFIG}
    fi
}

modify_scraper_config(){
    # $1: password of the database
    if [ -n "$1" ];then
        local passwd_pattern='"db_password":.*'
        local passwd_setting="\"db_password\": \"$1\","
        sed -i "s/${passwd_pattern}/${passwd_setting}/g" ${SCRAPER_CONFIG}
    fi

    local log_pattern='"error_log":.*'
    local log_setting="\"error_log\": \"\/src\/scraper_error.log\""

    sed -i "s/${log_pattern}/${log_setting}/g" ${SCRAPER_CONFIG}
}

modify_docker_compose_config(){
    # $1: password of the database
    if [ -n "$1" ];then
        local pattern="POSTGRES_PASSWORD:.*"
        local setting="POSTGRES_PASSWORD: $1"

        sed -i "s/${pattern}/${setting}/g" ${DOCKER_COMPOSE_CONFIG}
    fi
}

delete_all_current_containers(){
    containers=$(docker ps -a -q)

    if [ -n "${containers}" ]; then
        docker stop ${containers}
        docker rm ${containers}
    fi

}

start_service(){
    cd ${DOCKER_COMPOSE_DIR}
    docker-compose up -d $@
}

stop_service(){
    cd ${DOCKER_COMPOSE_DIR}
    docker-compose stop
}

cleanup(){
    stop_service
    delete_all_current_containers
    rm -rf ${CONF_BACKUP_DIR}
}

get_ip(){
    echo `ip -o addr show scope global |grep -v docker |grep -v br- | awk '{gsub(/\/.*/, " ",$4); print $4}'`
}

prompt_for_hostname(){
    local ip
    read -p "Please input a hostname or ip address (will use local ip if not provided): " ip

    if [ -z "$ip" ]; then
        ip=`get_ip`
    fi
    echo $ip
}

prompt_for_db_password(){
    local password
    read -p "Please input the password of the database (will use current settings if not provided): " password
    echo $password
}

case "$1" in
    setup)
        hostname_or_ip=`prompt_for_hostname`
        db_password=`prompt_for_db_password`

        if [ "$2" = "clean" ]; then
            restore_all_configs
            cleanup
            clone_or_update_project_sources
        fi

        # build_base_image

        copy_pip_requirements_for_building_images

        backup_all_configs

        modify_django_config "${hostname_or_ip}" "${db_password}"
        modify_scraper_config "${db_password}"
        modify_docker_compose_config "${db_password}"

        start_service --build
        ;;
    start)
        start_service
        ;;
    stop)
        stop_service
        ;;
    restore)
        restore_all_configs
        ;;
    cleanup)
        restore_all_configs
        cleanup
        ;;
    *)
        echo "Usage: $0 { setup | setup clean | start | stop | restore | cleanup }"
        exit 1
esac
exit
