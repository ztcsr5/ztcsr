# ztcsr Music Suite

一个高级的命令行音乐软件，提供曲库管理、播放列表、均衡器以及推荐系统等功能。该项目以 Python 编写，能够快速导入曲目、模拟播放流程，并生成个性化推荐。

## 功能亮点

- **曲库管理**：支持导入、搜索、更新曲目信息，自动持久化到本地 JSON 存储。
- **播放模拟**：可处理播放队列、跨曲目淡入淡出、跳过与回放等操作，同时记录详细的播放事件历史。
- **均衡器系统**：内置多种 EQ 预设并支持渐变过渡，方便根据氛围动态调整音效。
- **智能推荐**：基于曲目流行度与情绪标签的混合推荐算法，提供心情筛选和热门趋势列表。

## 快速开始

1. **安装依赖**

   ```bash
   pip install -e .[dev]
   ```

2. **查看帮助信息**：任意时候可使用 `-h/--help` 获取可用子命令与参数。

   ```bash
   python -m music_app.cli --help
   ```

3. **导入曲目数据**：项目附带了示例曲库，首次使用可直接导入。

   ```bash
   python -m music_app.cli import examples/sample_tracks.json
   ```

4. **浏览曲库**：列出全部曲目或通过 `--filter` 关键字匹配标题、艺术家或情绪标签。

   ```bash
   python -m music_app.cli list
   python -m music_app.cli list --filter "calm"
   ```

5. **创建或播放播放列表**：播放命令既可读取示例文件，也可以指向你自己编写的 JSON 播放列表。

   ```bash
   python -m music_app.cli play examples/sample_playlist.json
   ```

   自定义播放列表示例结构：

   ```json
   {
     "name": "Focus Session",
     "tracks": ["track_id_1", "track_id_2"],
     "crossfade": 4
   }
   ```

6. **应用均衡器预设**：在播放过程中可通过 `--eq` 指定 EQ 预设名称（如 `warm`、`bright`）。

   ```bash
   python -m music_app.cli play examples/sample_playlist.json --eq warm
   ```

7. **获取推荐**：按照心情或趋势筛选推荐曲目。

   ```bash
   python -m music_app.cli recommend mood calm
   python -m music_app.cli recommend trending
   ```

8. **查看播放历史**：导入与播放后，可使用以下命令查看最近的播放事件。

   ```bash
   python -m music_app.cli history --limit 10
   ```

9. **重置数据**：如果想清空曲库与播放记录，可使用 `reset` 命令。

   ```bash
   python -m music_app.cli reset
   ```

## 运行测试

```bash
pytest
```

## 许可证

MIT
