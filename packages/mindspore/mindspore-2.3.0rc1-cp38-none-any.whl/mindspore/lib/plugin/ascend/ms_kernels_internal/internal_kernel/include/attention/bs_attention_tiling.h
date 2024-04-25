#ifndef __BS_ATTENTION_TILING_H__
#define __BS_ATTENTION_TILING_H__

#pragma pack (8)
typedef struct {
    uint64_t batch_size;
    uint64_t num_heads;
    uint64_t max_seqlen;
    uint64_t head_dim;
    uint64_t num_group;
    uint64_t q_seqlen;
    uint64_t kv_seqlen;
    uint64_t table_block_size;
    uint64_t sync_addr;
    uint64_t core_num;
    float tor;
} BSAttentionTilingData;
#pragma pack()

#define MAX_CORE_NUM 25
#define ATTENTION_DEBUG false // 开启时会对S/P写入调试数据
#define BUFFER_NUM 2 // 核间流水数，暂不支持修改

#if PA
#define INC true
#define OP_NAME PagedAttention
#else
#define INC false
#define OP_NAME FlashAttentionScore
#endif

#if BFLOAT16
#define TYPE_NAME _bf16
#else
#define TYPE_NAME _fp16
#endif

#if BSH
#define LAYOUT_NAME _BSH
#else
#define LAYOUT_NAME _BNSD
#endif

#define CONCAT_(A, B, C, D) A##B##C##D
#define CONCAT(A, B, C, D) CONCAT_(A, B, C, D)
#define FUNC_NAME_AIC CONCAT(OP_NAME, TYPE_NAME, LAYOUT_NAME, _mix_aic)
#define FUNC_NAME_AIV CONCAT(OP_NAME, TYPE_NAME, LAYOUT_NAME, _mix_aiv)

#if INC
#define CORE_PER_KV_HEAD 4 // 增量推理时开启，每个kv_head切分成多少个任务计算
#endif

// **************mask patten模式**************//
// 第一种：下三角，开启LOWER_TRIANGLE时会直接采用下三角，不依赖mask
// #define LOWER_TRIANGLE false

// 第二种：Block Sparse，LOWER_TRIANGLE关闭时，开启BLOCK_SPARSE，会使用pre_token和next_token，不依赖mask（待开发）
// #define BLOCK_SPARSE false

// 第三种：读取MASK，LOWER_TRIANGLE和BLOCK_SPARSE关闭时，开启AMASK，会使用mask作为输入
// #define AMASK true

// 第四种：全矩阵，LOWER_TRIANGLE、BLOCK_SPARSE和AMASK如果全部关闭，则此attention采用全矩阵运算，不抑制S中的元素
// *******************************************//

constexpr uint64_t WORKSPACE_MAX_SEQLEN = 10240;    // max seqlen: 10240
constexpr uint64_t WORKSPACE_MAX_SEQLEN_BLOCK = WORKSPACE_MAX_SEQLEN / 16;    // max seqlen: 10240
constexpr uint64_t WORKSPACE_SIZE = 128 * WORKSPACE_MAX_SEQLEN; 
constexpr uint64_t BUFFER_SIZE = MAX_CORE_NUM * WORKSPACE_SIZE * sizeof(uint16_t);

#endif