# Vagrantfile
Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/focal64"
  
  # Puerto 8000 expuesto automáticamente
  config.vm.network "forwarded_port", guest: 8000, host: 8000
  config.vm.network "private_network", ip: "192.168.56.10"

  # PROVISIONAMIENTO AUTOMÁTICO
  config.vm.provision "shell", inline: <<-SHELL
    # 1. Instalación de dependencias
    echo "--- Actualizando sistema e instalando Python ---"
    apt-get update
    apt-get install -y python3-pip ntpdate ca-certificates
    
    # Sincronizar hora (CRUCIAL para la API de IONOS)
    ntpdate time.google.com
    
    # Instalar librerías de Python
    pip3 install fastapi uvicorn requests jinja2 python-multipart

    # Desactivar firewall
    ufw disable
    
    # Crear carpetas de datos
    mkdir -p /vagrant/data
    if [ ! -f /vagrant/data/pending_records.json ]; then echo "[]" > /vagrant/data/pending_records.json; fi
    if [ ! -f /vagrant/data/synced_records.json ]; then echo "[]" > /vagrant/data/synced_records.json; fi
    
    # Dar permisos totales a la carpeta data para evitar errores de escritura
    chmod -R 777 /vagrant/data

    # 2. CONFIGURAR AUTO-ARRANQUE DEL SERVIDOR WEB (Systemd)
    echo "--- Configurando servicio Web automático ---"
    cat <<EOT > /etc/systemd/system/urlshortener.service
[Unit]
Description=URL Shortener Web Server
After=network.target

[Service]
User=vagrant
WorkingDirectory=/vagrant
ExecStart=/usr/local/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
EOT

    # Recargar servicios y arrancar la web
    systemctl daemon-reload
    systemctl enable urlshortener
    systemctl start urlshortener

    # 3. CONFIGURAR AUTO-EJECUCIÓN DEL WORKER (Cron)
    echo "--- Configurando Cron para sincronización con IONOS ---"
    # Crea una tarea que ejecuta el script cada minuto y guarda log en /vagrant/cron.log
    echo "* * * * * vagrant /usr/bin/python3 /vagrant/sync_dns.py >> /vagrant/cron.log 2>&1" > /etc/cron.d/ionos_sync
    chmod 644 /etc/cron.d/ionos_sync

    echo "--- ¡INSTALACIÓN COMPLETADA! ---"
    echo "Ya puedes entrar a http://192.168.56.10:8000"
  SHELL
end