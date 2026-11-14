# FROM ros:foxy-ros-base-focal
# FROM ros:galactic-ros-base-focal
# FROM ros:humble-ros-base-jammy
# FROM ros:jazzy-ros-base-noble
FROM ros:lyrical-ros-base-resolute

LABEL maintainer="Waipot Ngamsaad <waipotn@hotmail.com>"

SHELL ["/bin/bash", "-c"]

ENV DEBIAN_FRONTEND noninteractive

# install Ubuntu packages
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y \
    curl \
    git \
    wget \
    nano \
    sudo \
    bash-completion \
    htop \
    tmux \
    terminator \
    xfe \
    openbox \
    tint2 \
    feh \
    wmctrl \
    xfonts-base \
    xauth \
    x11-xkb-utils \
    xkb-data \
    dbus-x11 \
    net-tools \
    iputils-ping \
    usbutils \
    tigervnc-standalone-server \
    tigervnc-xorg-extension \
    novnc \
    python3-dev \
    python3-pip \
    python3-numpy \
    python3-scipy \
    ffmpeg \
    libgbm-dev \
    libnss3-dev \
    libssl-dev \
    libffi-dev \
    libi2c-dev \
    build-essential \
    && chmod u+s /usr/bin/bwrap 2>/dev/null || true \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# install ROS packages
RUN apt-get update --fix-missing && apt-get upgrade --fix-missing -y && \
    apt-get install -y \
    ros-${ROS_DISTRO}-desktop-full \
    ros-${ROS_DISTRO}-rviz-imu-plugin \
    python3-rosdep \
    python3-colcon-common-extensions \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# init rosdep
RUN rm -f /etc/ros/rosdep/sources.list.d/20-default.list && \
    rosdep init && \
    rm -f /etc/apt/apt.conf.d/docker-clean

# install supervisor
RUN pip3 install -U --no-cache-dir --break-system-packages \
    libconf \
    supervisor \
    supervisor_twiddler

RUN apt-get update && apt-get install -y openssh-server && \
    mkdir -p /var/run/sshd && \
    sed -i 's/^#Port 22/Port 3333/' /etc/ssh/sshd_config && \
    echo 'PermitRootLogin yes' >> /etc/ssh/sshd_config && \
    echo 'PasswordAuthentication yes' >> /etc/ssh/sshd_config
    
# set password for ubuntu user
RUN echo "ubuntu:ubuntu" | chpasswd

# setup user space
RUN mkdir -p {/workspace,/app}

ARG USERNAME="ubuntu"
RUN echo "Creaing user: ${USERNAME}" && \
    # useradd -m ${USERNAME} && \
    usermod -aG sudo ${USERNAME} && \
    usermod --shell /bin/bash ${USERNAME} && \
    chown -R ${USERNAME}:${USERNAME} /workspace && \
    chown -R ${USERNAME}:${USERNAME} /app && \
    ln -sfn /workspace /home/${USERNAME}/workspace && \
    ln -sfn /app /home/${USERNAME}/app && \
    echo ${USERNAME} ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/${USERNAME} && \
    chmod 0440 /etc/sudoers.d/${USERNAME}

ENV USER ${USERNAME}

ENV HOME /home/${USERNAME}

ENV SHELL /bin/bash

ENV ROS_DOMAIN_ID=50

#========== USER SPACE ==========#
USER $USER

WORKDIR $HOME

# init rosdep
RUN rosdep fix-permissions && rosdep update

# enable bash completion
RUN echo "source /usr/share/bash-completion/bash_completion" >> ~/.bashrc && \
    echo "source ~/.bashrc" >> ~/.bash_profile && \
    echo "export ROS_DOMAIN_ID=50" >> ~/.bashrc

RUN mkdir -p /workspace/dev_ws/src && \
    cd /workspace/dev_ws && \
    source /opt/ros/${ROS_DISTRO}/setup.bash && \
    colcon build --symlink-install && \
    echo "DONE"

# https://superuser.com/questions/555310/bash-save-history-without-exit
RUN echo "export PROMPT_COMMAND='history -a'" >> ~/.bashrc && \ 
    echo "source /usr/share/colcon_argcomplete/hook/colcon-argcomplete.bash" >> ~/.bashrc && \
    echo "source /opt/ros/$ROS_DISTRO/setup.bash" >> ~/.bashrc && \
    echo "source /workspace/dev_ws/install/setup.bash" >> ~/.bashrc && \
    echo "Done"

COPY ./test_imu.rviz /home/${USERNAME}/
COPY ./view_imu.sh /home/${USERNAME}/

COPY ./index.html /usr/share/novnc
COPY ./app/install/code-server.sh /app/install/

# install code-server
RUN /app/install/code-server.sh 4.23.1 && \
    /usr/bin/code-server --install-extension ms-toolsai.jupyter

# Install ipykernel for Python Jupyter support
RUN pip3 install --break-system-packages ipykernel

COPY ./app /app
RUN sudo chown -R ${USERNAME}:${USERNAME} /app && \
    sudo ln -sf /app/supervisord.conf /etc/supervisord.conf && \
    sudo usermod -aG dialout ${USERNAME} && \
    sudo usermod -aG video ${USERNAME} && \
    sudo usermod -aG i2c ${USERNAME} && \
    # sudo groupmod -g 998 i2c
    echo "\n"

VOLUME /tmp/.X11-unix

ENV DISPLAY ":9"

EXPOSE 8001 6901 3333

# clean
RUN sudo apt-get -y autoremove && \
    sudo apt-get clean && \
    sudo rm -rf /var/lib/apt/lists/*

# Install Antigravity CLI (only supported on 64-bit architectures)
USER ubuntu
RUN ARCH=$(uname -m); \
    if [ "$ARCH" = "x86_64" ] || [ "$ARCH" = "aarch64" ]; then \
        curl -fsSL https://antigravity.google/cli/install.sh | bash; \
    else \
        echo "Skipping Antigravity CLI install: not supported on $ARCH"; \
    fi

# Configure Antigravity CLI to auto-accept tools and shell commands
RUN mkdir -p /home/ubuntu/.gemini/antigravity-cli && \
    cat > /home/ubuntu/.gemini/antigravity-cli/settings.json << 'EOF'
{
  "toolPermission": "always-proceed",
  "artifactReviewPolicy": "always-proceed",
  "enableTerminalSandbox": false,
  "allowNonWorkspaceAccess": true,
  "permissions": {
    "allow": [
      "command(*)",
      "read_file(*)",
      "write_file(*)",
      "read_url(*)",
      "execute_url(*)",
      "mcp(*)",
      "shell(*)",
      "run_command(*)",
      "replace_file_content(*)",
      "create_file(*)"
    ]
  }
}
EOF

CMD ["sudo", "-E", "/usr/local/bin/supervisord", "-c", "/app/supervisord.conf"]
