#ifndef BS_FLASHATTENTION_BS__ATTENTION_MIX_HWSYNC_H
#define BS_FLASHATTENTION_BS__ATTENTION_MIX_HWSYNC_H
constexpr float DROPOUT_PROP = 0.5;
constexpr uint32_t LOOP_LEN = 5;
constexpr uint32_t UB_HALF_BUF_SIZE = 8 * 2048;
constexpr uint32_t BIT_UINT8 = 8;
constexpr uint32_t BIT_BLOCK = 256;
constexpr uint32_t BLOCK_SIZE = 16;
constexpr uint32_t VECTOR_SIZE = 128;
constexpr uint32_t VECTOR_SIZE_FP32 = 64;
constexpr uint32_t CUBE_MATRIX_SIZE = 256;// 16 * 16
constexpr uint64_t UB_UINT8_BLOCK_SIZE = 16384; // 64 * 128 * 2B
constexpr uint64_t UB_UINT8_LINE_SIZE = 512;    // 64 * 4B，申请两倍空间防踩踏。
constexpr uint64_t UB_FLOAT_LINE_SIZE = 128;    // 64，申请两倍空间防踩踏。
constexpr uint64_t UB_HALF_LINE_SIZE = 256;     // UB_FLOAT_LINE_SIZE * 2

constexpr uint32_t L0AB_HALF_BUF_SIZE = 16384; // 128 * 128
constexpr uint64_t L1_SIZE = 512 * 1024; // 512KB
constexpr uint64_t L0AB_UINT8_BLOCK_SIZE = 32768; // 128 * 128 * 2B
constexpr uint64_t L1_MAX_SHARE_NUM = (L1_SIZE - 8 * L0AB_UINT8_BLOCK_SIZE) / L0AB_UINT8_BLOCK_SIZE / 2; 
constexpr uint64_t SUB_SP_SIZE = 2048 * 8;  // 1024*16, 2048*8, 4096*4, 8192*2, 16K*1，五种分块方法

enum class L1Mode{load, // 读取数据至L1的share区
                  share, // 使用share区的数据
                  noshare};  // 不读且不用share区

inline uint64_t ceil(uint64_t y, uint64_t x) {
    return (y + x - 1) / x;
}

inline uint64_t round(uint64_t y, uint64_t x) {
    return ceil(y, x) * x;
}

#if BFLOAT16
#define CALC_DATA_TYPE bfloat16_t
#else 
#define CALC_DATA_TYPE half
#endif

#endif //BS_FLASHATTENTION_BS__ATTENTION_MIX_HWSYNC_H
