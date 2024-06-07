local config = import 'default.jsonnet';

config {
  'okami_9000-1'+: {
    cmd: 'okamid-rocksdb',    
    'app-config'+: {
      'app-db-backend': 'rocksdb',      
      pruning: 'everything',
      'state-sync'+: {
        'snapshot-interval': 0,
      },
      'memiavl'+:{
        enable: true,
        'snapshot-keep-recent': 0,
        'snapshot-interval': 1,
      },
      'store'+: {
        streamers: [],
      },
    },
    config+: {
       'db_backend': 'rocksdb',
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
