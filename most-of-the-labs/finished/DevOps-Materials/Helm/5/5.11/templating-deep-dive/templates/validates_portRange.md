
{{- define "templating-deep-dive.validators.portRange" -}}
{{- /* expects a port as context */ -}}
{{- $sanitizedPort := int . -}}
{{- if or (lt $sanitizedPort 1) (gt $sanitizedPort 65535) }}
{{- fail "ports must be between 1 and 65535" }}
{{- end }}
{{- . }}
{{- end -}}