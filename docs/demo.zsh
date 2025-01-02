#!/usr/bin/env zsh

function type_string() {
  string=("$1")
  delay=${2:-0.05}
  for char in ${(s::)string}; do
    if [[ $char == "-" ]]; then
      echo -n - -
    else
      echo -en "$char"
    fi
    sleep $delay
  done
}

sleep 5
type_string "GPU=$GPU"; echo
type_string "AUD=$AUD"; echo
type_string 'lspci -nnk -d $GPU; lspci -nnk -d $AUD'; echo
sleep 0.5
type_string "# Unbinding the gpu and audio device drivers:"; echo
type_string 'sudo pearasys -v \'; echo
type_string '	-d $GPU -d $AUD \'; echo
type_string '	driver vfio-pci unbind'; echo
echo 'lspci -nnk -d $GPU; lspci -nnk -d $AUD'
sleep 0.5
type_string "# Binding non-vfio drivers: "; echo
type_string 'sudo modprobe nvidia'; echo
sleep 1
type_string 'sudo pearasys -v \'; echo
type_string '	driver -d $GPU nvidia bind \'; echo
type_string '	driver -d $AUD snd_hda_intel bind'; echo
echo 'lspci -nnk -d $GPU; lspci -nnk -d $AUD'
sleep 0.5
type_string "# FZF is used to select devices when none are provided through the CLI:"; echo
type_string 'sudo pearasys -v \'; echo
type_string '	device remove \'; echo
type_string '	rescan'
sleep 1
echo
sleep 0.5
type_string 'GP104'
sleep 1
echo -en $'\e'"[A"
sleep 0.25
echo -e '\t'
sleep 0.25
echo -e '\t'
sleep 0.25
echo -e '\r'
sleep 1
echo 'lspci -nnk -d $GPU; lspci -nnk -d $AUD'
sleep 0.5
type_string "# Driver overriding, dynamic ID matching, and other sysfs-bus-pci and sysfs-pci resources are available."; echo
type_string "# See pearasys --help for more information."; echo
sleep 2
echo "exit"
