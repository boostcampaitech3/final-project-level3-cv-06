checkpoint_config = dict(interval=1)
# yapf:disable
log_config = dict(
    interval=50,
    hooks=[
        dict(type='TextLoggerHook'),
        # dict(type='TensorboardLoggerHook')
        dict(type='WandbLoggerHook',interval=10,
            init_kwargs=dict(
                project='ARTLab_JHwan', #프로젝트명
                entity = 'omakase',      #고정
                name = 'tood_x101_cpDataV2_ep30_0_005_PAFPN_albu_cIoU'     #이름
            ),
        )         
    ])
# yapf:enable
custom_hooks = [dict(type='NumClassCheckHook')]

dist_params = dict(backend='nccl')
log_level = 'INFO'
load_from = None
resume_from = None
workflow = [('train', 1)]
