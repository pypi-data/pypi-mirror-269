#pragma once

#include <cstdint>
#include <set>
#include <vector>

namespace akida {

namespace np {

struct Ident {
  uint8_t col;
  uint8_t row;
  uint8_t id;
  bool operator==(const Ident& other) const {
    return col == other.col && row == other.row && id == other.id;
  }
  bool operator!=(const Ident& other) const { return !(*this == other); }
  bool operator<(const Ident& other) const {
    return (col < other.col) || ((col == other.col) && (row < other.row)) ||
           ((col == other.col) && (row == other.row) && (id < other.id));
  }
};

using IdentVector = std::vector<Ident>;

constexpr Ident HRC_IDENT = Ident{0, 0, 0};

enum class BasicType { none, HRC, CNP, FNP, VIT_NODE };
enum class Type { none, HRC, CNP1, CNP2, FNP2, FNP3, VIT_NODE };
using Types = std::set<Type>;

constexpr bool is_cnp(Type type) {
  return type == Type::CNP1 || type == Type::CNP2;
}

constexpr bool is_fnp(Type type) {
  return type == Type::FNP2 || type == Type::FNP3;
}

struct Info {
  Ident ident;
  Types types;
};

/**
 * The layout of a mesh of Neural Processors
 */
struct Mesh {
  np::Ident dma_event;       /**<The DMA event endpoint */
  np::Ident dma_conf;        /**<The DMA configuration endpoint */
  std::vector<np::Info> nps; /**<The available Neural Processors */
};

}  // namespace np

}  // namespace akida
