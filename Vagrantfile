# -*- mode: ruby -*-
# vi: set ft=ruby :

ENV['VAGRANT_SERVER_URL'] = 'https://vagrant.elab.pro'

Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/focal64"
  config.vm.hostname = "mysite"
  config.vm.network "private_network", ip: "192.168.56.10"
  config.vm.network "forwarded_port", host: 8888, guest: 80
end
