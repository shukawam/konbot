# Konbot - Kong Bot

This is a sample application that demonstrates Kong's AI-related plugins.

## Overview

```mermaid
flowchart LR

A1[Client - Browser] --> B1[Streamlit]
B1 --> C1[Kong AI Gateway]
C1 --> D1[LLMs - OpenAI]
C1 --> D2[Vector/Cache Store - Redis]
```

## How to run?

First, set up Kong Gateway and Redis.

```sh
docker compose up -d
deck gateway sync plugins/ai/kong.yaml
```

After that, run the following scripts to set up vector store.

```sh
plugin_id=`curl http://localhost:8001/plugins | jq -r '.data[] | select(.name == "ai-rag-injector").id | @text'`
curl --request POST \
  --url http://localhost:8001/ai-rag-injector/$plugin_id/ingest_chunk \
  --header 'content-type: application/json' \
  --data '{"content": "株式会社ゴリゴリ・スペースは、人類の宇宙への夢を加速させる、次世代の超大型ロケット**「ゴリラロケット」**を発表します。比類なき推進力と革新的なテクノロジーで、宇宙開発の新たなフロンティアを切り拓きます。\n1. 革新的なテクノロジー \n\n1.1. 超高効率ハイブリッドエンジン「マウンテン」従来の液体燃料と固体燃料の利点を融合した、テラフォーム・スペース独自のハイブリッドエンジンです。比推力450秒以上を達成し、圧倒的な推進効率を実現しました。再利用を前提とした設計により、運用コストの大幅な削減に貢献します。\n\n1.2. 自己進化型AI制御システム「コング」\n打ち上げから軌道投入、そして正確な着陸まで、ミッションの全フェーズをリアルタイムで最適化するAI制御システム。膨大なフライトデータとシミュレーション結果を学習し、予期せぬ状況にも柔軟に対応。人間の介入を最小限に抑え、ミッションの成功率と安全性を飛躍的に向上させます。\n\n1.3. 自己修復型ナノマテリアル\nロケットの機体構造には、自己修復機能を持つ新開発のナノマテリアルを採用しています。宇宙空間での微細なデブリ衝突による損傷や、打ち上げ時の極度の熱応力によるひび割れを自己的に修復。ロケットの耐久性と信頼性を劇的に高めます。\n\n1.4. 超軽量・高強度複合材\nカーボンナノチューブ技術を応用した、革新的な複合材を使用。これにより、ロケットの構造重量を極限まで軽量化しつつ、同時に比類なき強度と剛性を実現しました。ペイロード容量の最大化に貢献し、より多くの物資や人員を宇宙へ送り出すことを可能にします。\n\n2. ゴリラロケットが切り拓く未来\nゴリラロケットは、単なる輸送手段ではありません。それは、人類が宇宙へと本格的に進出するための、強力な基盤となります。\n大規模月面基地の建設: これまで不可能だった大量の資材やモジュールの輸送により、月面での大規模な居住施設や研究拠点の構築を加速します。\n有人火星探査の実現: 火星への長期滞在ミッションに必要な大型宇宙船や探査機、食料、水などを効率的に輸送し、人類の火星移住計画を現実のものとします。\n新たな宇宙産業の創出: 軌道上での製造、宇宙太陽光発電衛星の展開、小惑星からの資源採掘など、宇宙空間での新たなビジネスモデルの創出を強力に支援します。\n\n3. サービスラインナップ\n標準軌道投入サービス: LEO、GTO、SSOなど、多様な軌道へのペイロード投入。\n月面輸送サービス: 月周回軌道への物資投入、月面への直接着陸（将来的）。\n深宇宙探査ミッションサポート: 火星、木星など、深宇宙探査ミッション向けの特殊ペイロード打ち上げ。\nカスタマイズミッション: お客様の特定のニーズに合わせた、柔軟なミッション設計と打ち上げサービス。\n"}'
```

Finally, run the following script to start the LLM application.

```sh
uv pip install -e .
streamlit run main.py
```

Then, you can access [http://localhost:8501](http://localhost:8501) via your web browser.
