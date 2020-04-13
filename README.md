# zabbixBandwidthInfo

Coleta a banda das interfaces cadastradas no zabbix e envia para o telegram

## Configurações

Configure os aquivos interfaces.yml e config.ini

## Criando o build da imagem docker

```sh
docker build -t zabbixinfo:latest .

```

## Iniciando a imagem

```sh
docker run -d \
  --name zabbix_info \
  --mamory="64m" \
  --restart=always \
  zabbixinfo:latest
```
