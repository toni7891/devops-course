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
{{- end -}}

{{- /* Expects an integer or string to be passed as context */ -}}
{{- define "templating-deep-dive.validators.portRange" -}}
{{- $sanitizedPort := int . -}}
{{- /* Port Validation */ -}}
{{- if or (lt $sanitizedPort 1) (gt $sanitizedPort 65535) }}
{{- fail "ports must be between 1 and 65535" }}
{{- end }}
{{- end -}}


{{- /* Expects an object with port and type to be passed as context */ -}}
{{- define "templating-deep-dive.validators.service" -}}
{{- include "templating-deep-dive.validators.portRange" .port -}}

{{/* Service Type Validation */}}
{{- $allowedTypes := list "ClusterIP" "NodePort" -}}
{{- if not (has .type $allowedTypes) }}
{{- fail (printf "invalid service type %s. supported: %s" .type ($allowedTypes | join ", ")) }}
{{- end }}
{{- end -}}