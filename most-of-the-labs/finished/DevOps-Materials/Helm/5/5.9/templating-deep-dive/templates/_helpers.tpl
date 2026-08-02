{{- define "templating-deep-dive.fullname" -}}
{{- $fullname := printf "%s-%s" .Release.Name .Chart.Name }}
{{- if .Values.customName }}
{{- $fullname = .Values.customName }}
{{- end}}
{{- $fullname | trunc 63 | trimSuffix "-" }}
{{- end -}}

{{- define "templating-deep-dive.selectorLabels" -}}
app: {{ .Chart.Name }}
release: {{ .Release.Name }}
managed-by: "helm"
{{- end -}} end -}} end -}}