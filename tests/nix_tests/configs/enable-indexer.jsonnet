local config = import 'default.jsonnet';

config {
  'okami_9000-1'+: {
    config+: {
      tx_index+: {
        indexer: 'null',
      },
    },
    'app-config'+: {
      'json-rpc'+: {
        'enable-indexer': true,
      },
    },
    genesis+: {
      app_state+: {
        feemarket+: {
          params+: {
            min_gas_multiplier: '0',
          },
        },
      },
    },
  },
}