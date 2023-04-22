#!/usr/bin/env bash


function if_sludge_not_running(){
    # find 'sludge_client'  but not 'sludge_client_setup' process, then stop
    # ps -ef | grep 'sludge_client' | grep -v grep
    # if [ $? -eq 0 ]
    # then

    # if ps -ef | grep 'sludge_client' | grep -v grep; then  # can find sludge_client process

        # ps -ef | grep 'sludge_client_setup' | grep -v grep
        # if [ $? -ne 0 ]
        # then
        # if !(ps -ef | grep 'sludge_client_setup' | grep -v grep); then  # but not find sludge_client_setup process
    echo ""
    if (ps -ef | grep 'sludge_client' | grep -v grep) && !(ps -ef | grep 'sludge_client_setup' | grep -v grep); then
        echo " -> Sludge Client is running, please close the program and try again!"
        # sleep 7
        # runing='true'
        return 1  # un normal
        # fi
    else
        return 0  # normal
    fi
}


function mk_program_dir(){

    if [ ! -d /opt/${program_name} ]; then  # only mk dir if it is not exist
        mkdir /opt/${program_name}
        echo " -> Sludge Client program folder has been created."
        # echo ""
    # else
    #     echo " -> Sludge Client program folder already exists."
        # echo ""
    fi

    # if [ ! -d /home/$USER/.${program_name} ]; then  # 新建项目文件夹
    # if [ ! -d /home/$SUDO_USER/.${program_name} ]; then  # 新建项目文件夹
    #     # mkdir ~/.${program_name}
    #     mkdir /home/$SUDO_USER/.${program_name}
    #     echo " -> Sludge Client data folder has been created."
    #     # echo ""
    # else
    #     echo " -> Sludge Client data folder already exists."
    #     # echo ""
    # fi

    # rm -rf ~/.${program_name}/bin  # 删除 bin 文件夹, 后续下载后重新建立

    # if [ ! -d /home/$USER/.sludge_client/bin ]; then
    #     mkdir ~/.sludge_client/bin
    #     echo " -> Sludge client program folder has been created."
    # else
    #     echo " -> Sludge client program folder already exists."
    # fi

    # if [ ! -d /home/$USER/.${program_name}/projects ]; then  # 新建项目文件夹
    #     mkdir ~/.${program_name}/projects
    #     echo " -> Sludge working folder has been created."
    # else
    #     echo " -> Sludge working folder already exists."
    # fi
    # if [ ! -d /home/$USER/.local/bin ]; then
    if [ ! -d /home/$SUDO_USER/.local/bin ]; then  # only mk dir if it is not exist
        mkdir /home/$SUDO_USER/.local/bin
        # echo " -> local bin folder has been created."
        # echo ""
    # else
        # echo " -> local bin folder already exists."
        # echo ""
    fi

}


function mk_data_dir(){  # should mk later than mk_program_dir
    if [ ! -d /home/$SUDO_USER/.${program_name} ]; then  # only mk dir if it is not exist
        mkdir /home/$SUDO_USER/.${program_name}
        echo " -> Sludge Client data folder has been created."
        # echo ""
    else
        echo " -> Sludge Client data folder already exists."
        # echo ""
    fi
}


function rm_program_dir(){  # # remove folder if exist

    if [ -d /opt/${program_name} ]; then
        rm -rf /opt/${program_name}
        echo " -> Sludge Client program folder has been removed."
        # echo ""
    fi

}


function download_untar(){  # 下载解压主程序
    # cd /home/$SUDO_USER/.local/bin
    # 下载解压后改名, 最后删除
    # wget -O ${program_name}.tar.xz $main_url/api/download/client/linux

    release_os=$(lsb_release -i --short)
    release_num=$(lsb_release -r --short)

    if [[ $release_os =~ 'Ubuntu' ]]; then
        if [[ $release_num =~ '16' ]] || [[ $release_num =~ '18' ]]; then
            download_url=$main_url/api/download/client/linux/ubuntu1618
        else
            download_url=$main_url/api/download/client/linux/ubuntu20
        fi
    fi

    if wget -O ${program_name}.tar.xz $download_url ; then
        tar -xvf ${program_name}.tar.xz
        # mv ${program_name}.dist bin
        mv ${program_name}.dist/* /opt/${program_name}
        rm -r ${program_name}.dist
        rm ${program_name}.tar.xz

        # cd bin
        chmod -R 777 ${program_name}
        echo " -> Sludge Client has been downloaded and created."
        # echo ""
        ln -fs /opt/${program_name}/${program_name} /home/$SUDO_USER/.local/bin/
        return 0  # normal
    else
       echo ' -> Cannot download Sludge Client right now, please try again later or contact to the administrator.'
    #    echo ""
       return 1  # un normal
    fi
}


function mk_uninstall(){  # run uninstall by: sudo /opt/sludge_client/uninstall.sh
    echo "#!/usr/bin/env bash" > uninstall.sh
    echo "" >> uninstall.sh
    echo "" >> uninstall.sh

    echo "function if_sludge_not_running(){" >> uninstall.sh
    echo "    echo ''" >> uninstall.sh
    echo "    if ps -ef | grep 'sludge_client' | grep -v grep && !(ps -ef | grep 'sludge_client/uninstall' | grep -v grep); then" >> uninstall.sh
    echo "        echo ' -> Sludge Client is running, please close the program and try again!'" >> uninstall.sh
    echo "        return 1  # un normal" >> uninstall.sh
    echo "    else" >> uninstall.sh
    echo "        return 0  # normal" >> uninstall.sh
    echo "    fi" >> uninstall.sh
    echo "}" >> uninstall.sh
    echo "" >> uninstall.sh
    echo "" >> uninstall.sh

    echo "function uninstall(){" >> uninstall.sh
    echo "    echo ''" >> uninstall.sh
    echo "    echo '>>> Removing Sludge Client... <<<'" >> uninstall.sh
    echo "    echo ''" >> uninstall.sh

    echo "    read -p ' -> Do you want to remove Sludge Client data folder? [y/N] ' choice_remove" >> uninstall.sh
    echo "    if [ -z \$choice_remove ]; then  # if empty or N" >> uninstall.sh
    # echo "        :  # pass" >> uninstall.sh
    echo "        echo '  -> Keep the Sludge client data folder, you can remove it manually in: ~/.sluge_client'" >> uninstall.sh
    echo "    elif [ \$choice_remove == 'y' ] || [ \$choice_remove == 'Y' ]; then  # y/Y" >> uninstall.sh
    echo "        rm -f -r "/home/$SUDO_USER/.${program_name} >> uninstall.sh
    echo "        echo ' -> Sludge client data folder has been removed. <<<'" >> uninstall.sh
    echo "    fi" >> uninstall.sh
    echo "    echo ''" >> uninstall.sh

    # echo "rm -f -r ~/.sludge_client" >> uninstall.sh
    echo "    rm -f -r /opt/"${program_name} >> uninstall.sh
    echo "    echo ' -> Sludge client program folder has been removed. <<<'" >> uninstall.sh
    # echo "    rm -f ~/.local/bin/sludge_client" >> uninstall.sh
    echo "    rm -f "/home/$SUDO_USER/.local/bin/${program_name} >> uninstall.sh
    echo "    echo ' -> Sludge client executable program link has been removed. <<<'" >> uninstall.sh
    echo "    rm -f "/home/$SUDO_USER/.local/share/applications/${program_name}".desktop" >> uninstall.sh
    echo "    echo ' -> Sludge client desktop file has been removed. <<<'" >> uninstall.sh
    echo "    echo ''" >> uninstall.sh
    echo "    echo '>>> Sludge client has been removed successfully. <<<'" >> uninstall.sh
    echo "}" >> uninstall.sh
    echo "" >> uninstall.sh
    echo "" >> uninstall.sh

    # echo "runing='false'" >> uninstall.sh
    # echo "if_process_running" >> uninstall.sh
    # echo "if [ ${runing} == 'false' ]" >> uninstall.sh
    # echo "then" >> uninstall.sh
    echo "read -p ' -> Do you want to remove Sludge Client? [y/N] ' choice_uninstall" >> uninstall.sh
    echo "if [ -z \$choice_uninstall ]  # if empty or N" >> uninstall.sh
    echo "then" >> uninstall.sh
    echo "    :  # pass" >> uninstall.sh
    echo "elif [  \$choice_uninstall == 'y' ] || [  \$choice_uninstall == 'Y' ]; then  # y/Y" >> uninstall.sh
    echo "    if if_sludge_not_running; then  # only start while not calculation is running" >> uninstall.sh
    echo "        uninstall" >> uninstall.sh
    echo "    fi" >> uninstall.sh
    echo "fi" >> uninstall.sh
    echo "" >> uninstall.sh

    chmod -R 777 uninstall.sh
    echo " -> Sludge client uninstall shell has been created."
    # echo ""
    echo "" >> uninstall.sh
}


function make_url_protocol(){  # url 协议中不能带下划线!
    cd /home/$SUDO_USER/.local/share/applications
    # cd /usr/share/applications
    echo "[Desktop Entry]" > ${program_name}.desktop
    echo "Version=1.0" >> ${program_name}.desktop
    echo "Name=SludgeClient" >> ${program_name}.desktop
    echo "GenericName="${program_name} >> ${program_name}.desktop
    echo "Comment=sludge calculation callable function" >> ${program_name}.desktop
    echo "Type=Application" >> ${program_name}.desktop
    echo "Exec="${program_name}" %u" >> ${program_name}.desktop  # 这里放实际命令, 而不是 url 协议
    echo "Icon=/opt/sludge_client/package/icon/sludge_logo1a.png" >> ${program_name}.desktop  # 这里放实际命令, 而不是 url 协议
    echo "Terminal=false" >> ${program_name}.desktop
    echo "StartupNotify=false" >> ${program_name}.desktop
    echo "MimeType=x-scheme-handler/sludgeclient" >> ${program_name}.desktop  # url 协议中不能带下划线!
    update-desktop-database /home/$SUDO_USER/.local/share/applications
    # update-desktop-database /usr/share/applications
    echo " -> Sludge Client desktop file has been created."
    # echo ""
}


function main(){

    if [ -z $SUDO_USER ]  # must run this shell with 'sudo'
    then
        echo " -> Please run Sludge Client Setup with 'sudo'"
    else

        # main_url=http://127.0.0.1:5000
        # main_url=http://localhost:9000
        main_url=http://111.230.245.215:80
        program_name='sludge_client'
        can_remove='false'
        # runing='false'  # 默认 sluge client 没有在运行

        # if_process_running
        # if [ ${runing} == 'false' ]  #　不在运行才进行安装
        # then

        if if_sludge_not_running; then  # only start while not calculation is running
            echo ""
            echo ">>> Sludge Client is installing... <<<"
            echo ""

            # mk_program_dir

            # if !(cd /opt/${program_name}); then  # only mk dir if it is not exist
            if [ ! -d /opt/${program_name} ]; then  # only mk dir if it is not exist
                mk_program_dir
                can_remove='true'
            fi

            cd /opt/${program_name}
            if download_untar; then
                mk_data_dir
                mk_uninstall
                make_url_protocol
                echo ""
                echo ">>> Sludge Client has been installed successfully. <<<"
            else
                ${can_remove} == 'true' && rm_program_dir  # only remove when create program folder from not exist
                echo ""
                echo ">>> Sludge Client failed to install, please try again later. <<<"
            fi
        fi
    fi

}

main
