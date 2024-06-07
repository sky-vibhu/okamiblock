local config = import 'default.jsonnet';

config {
  'okami_9000-1'+: {
    config+: {
      storage: {
        discard_abci_responses: true,
      },
    },
  },
}
