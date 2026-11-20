#!/usr/bin/env bash

# Source ROS 2 and workspace environment
if [ -f "/opt/ros/${ROS_DISTRO:-lyrical}/setup.bash" ]; then
  source "/opt/ros/${ROS_DISTRO:-lyrical}/setup.bash"
fi
if [ -f "/workspace/dev_ws/install/setup.bash" ]; then
  source "/workspace/dev_ws/install/setup.bash"
fi

# Wait for X server to be ready
until xset q >/dev/null 2>&1; do
  sleep 0.2
done

# Configure US/Thai keyboard layout switching (Alt+Shift)
setxkbmap -layout "us,th" -option "grp:alt_shift_toggle" 2>/dev/null || true

# Setup default openbox config if not present
mkdir -p "$HOME/.config/openbox"
if [ ! -f "$HOME/.config/openbox/rc.xml" ] && [ -d /etc/xdg/openbox ]; then
  cp -r /etc/xdg/openbox/* "$HOME/.config/openbox/" 2>/dev/null || true
fi

# Use custom right-click menu and rc config if available
if [ -f /app/openbox/menu.xml ]; then
  cp /app/openbox/menu.xml "$HOME/.config/openbox/menu.xml"
fi
if [ -f /app/openbox/rc.xml ]; then
  cp /app/openbox/rc.xml "$HOME/.config/openbox/rc.xml"
fi

# Use custom tint2 config if available
mkdir -p "$HOME/.config/tint2"
if [ -f /app/tint2/tint2rc ]; then
  cp /app/tint2/tint2rc "$HOME/.config/tint2/tint2rc"
fi

# Sync bundled Antigravity CLI skills into persistent ~/.gemini volume
if [ -d /app/gemini/skills ]; then
  mkdir -p "$HOME/.gemini/config/skills"
  cp -r /app/gemini/skills/* "$HOME/.gemini/config/skills/" 2>/dev/null || true
fi

# Auto-refresh wallpaper when resolution changes
(
  PREV_RES=""
  while true; do
    CURR_RES=$(xrandr 2>/dev/null | grep '\*' | awk '{print $1}')
    if [ "$CURR_RES" != "$PREV_RES" ] && [ -n "$CURR_RES" ]; then
      PREV_RES="$CURR_RES"
      if [ -f /app/bg.png ]; then
        feh --bg-center /app/bg.png 2>/dev/null || true
      fi
    fi
    sleep 0.2
  done
) &

# Start tint2 taskbar
tint2 &

# Start Openbox window manager
exec openbox-session

