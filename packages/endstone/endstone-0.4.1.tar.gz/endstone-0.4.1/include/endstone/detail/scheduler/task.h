// Copyright (c) 2024, The Endstone Project. (https://endstone.dev) All Rights Reserved.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#pragma once

#include <chrono>
#include <functional>

#include "endstone/plugin/plugin.h"
#include "endstone/scheduler/task.h"

namespace endstone::detail {

class EndstoneTask : public Task {
private:
    using TaskClock = std::chrono::steady_clock;

public:
    using CreatedAt = std::chrono::time_point<TaskClock>;
    explicit EndstoneTask(Plugin &plugin, std::function<void()> runnable, TaskId task_id, std::uint64_t period);

    ~EndstoneTask() override = default;

    std::uint32_t getTaskId() override;
    Plugin &getOwner() override;
    bool isSync() override;
    bool isCancelled() override;
    void cancel() override;

    void run() const;
    [[nodiscard]] CreatedAt getCreatedAt() const;
    [[nodiscard]] std::uint64_t getPeriod() const;
    void setPeriod(std::uint64_t period);
    [[nodiscard]] std::uint64_t getNextRun() const;
    void setNextRun(std::uint64_t next_run);
    [[nodiscard]] const std::shared_ptr<EndstoneTask> &getNext() const;
    void setNext(std::shared_ptr<EndstoneTask> next);

private:
    Plugin &plugin_;
    std::function<void()> runnable_;
    TaskId task_id_;

    CreatedAt created_at_{TaskClock::now()};
    std::uint64_t period_;
    std::uint64_t next_run_;
    std::shared_ptr<EndstoneTask> next_;
};

}  // namespace endstone::detail
