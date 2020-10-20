# -*- mode: ruby -*-
# vi: set ft=ruby :

require 'yaml'

# Output utils
def colorize(text, color_code)
  "\e[#{color_code}m#{text}\e[0m"
end
def red(text); colorize(text, 31); end


Vagrant.configure(2) do |config|
  config.vm.box = "torchbox/wagtail-stretch64"
  config.vm.box_version = "~> 1.0"

  if Vagrant.has_plugin?("vagrant-vbguest")
    # Workaround to prevent missing linux headers making new installs fail.
    # Adapted from https://github.com/dotless-de/vagrant-vbguest/issues/351#issuecomment-536282015
    class WorkaroundVbguest < VagrantVbguest::Installers::Linux
      def install(opts=nil, &block)
        puts 'Ensuring we\'ve got the correct build environment for vbguest...'
        communicate.sudo('apt-get -y --force-yes update', (opts || {}).merge(:error_check => false), &block)
        communicate.sudo('apt-get -y --force-yes install -y build-essential linux-headers-amd64 linux-image-amd64', (opts || {}).merge(:error_check => false), &block)
        puts 'Continuing with vbguest installation...'
        super
        puts 'Performing vbguest post-installation steps...'
        communicate.sudo('usermod -a -G vboxsf vagrant', (opts || {}).merge(:error_check => false), &block)
      end
      def reboot_after_install?(opts=nil, &block)
        true
      end
    end
    config.vbguest.installer = WorkaroundVbguest
    # End workaround
  end


  config.vm.provision :shell, :path => "vagrant/provision.sh", :args => "torchbox"

  # Enable agent forwarding over SSH connections.
  config.ssh.forward_agent = true

  if File.exist? "Vagrantfile.local"
    instance_eval File.read("Vagrantfile.local"), "Vagrantfile.local"
  end
end
