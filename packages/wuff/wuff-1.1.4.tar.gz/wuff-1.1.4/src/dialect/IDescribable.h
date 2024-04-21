//
// Created by Michal Janecek on 28.01.2024.
//

#ifndef WUFF_IDESCRIBABLE_H
#define WUFF_IDESCRIBABLE_H

#include <string>

class IDescribable {
public:
    virtual ~IDescribable() = default;
    [[nodiscard]] virtual std::string getDescription() const = 0;
    [[nodiscard]] virtual std::string getName() const = 0;
};

#endif //WUFF_IDESCRIBABLE_H
