helm upgrade my-release bitnami/wordpress \
  --values custom-values.yaml \
  --reuse-values \


# Flag --atomic has been deprecated, use --rollback-on-failure instead
helm upgrade my-release bitnami/wordpress \
  --reuse-values \
  --values custom-values.yaml \
  --set image.tag=non-existent \
  --atomic \
  --cleanup-on-fail \
  --debug \
  --timeout 2m