#!/bin/bash

# Добавляем репозиторий (команда должна быть в одну строку)
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts

# Обновляем локальный кэш чартов
helm repo update

# Устанавливаем стек мониторинга (переносы строк оформлены через \)
helm upgrade monitoring \
  prometheus-community/kube-prometheus-stack \
  -n monitoring \
  --create-namespace
