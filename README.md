# Slack勤怠管理ボット

このSlackボットは、従業員の勤怠を管理し、勤務時間の記録、休憩時間の管理、スケジュールの設定、タスクの管理、休暇の申請などの機能を提供します。

## 主な機能

- 勤務開始・終了の記録
- 休憩時間の管理
- スケジュール管理
- タスク管理
- 休暇申請
- 週次・月次レポートの生成
- 勤務パターンの分析

## セットアップ

1. リポジトリをクローンします：
   ```
   git clone https://github.com/your-username/attendance-management-bot.git
   cd attendance-management-bot
   ```

2. 依存関係をインストールします：
   ```
   pip install -r requirements.txt
   ```

3. 環境変数を設定します：
   `.env`ファイルをプロジェクトのルートディレクトリに作成し、以下の内容を記入します：
   ```
   BOT_TOKEN=xoxb-your-bot-token
   APP_TOKEN=xapp-your-app-token
   AWS_REGION=us-east-1
   DYNAMODB_ENDPOINT=https://dynamodb.us-east-1.amazonaws.com
   ```

4. AWS CLIを設定します：
   ```
   aws configure
   ```

5. Serverless Frameworkをインストールします：
   ```
   npm install -g serverless
   ```

6. デプロイします：
   ```
   serverless deploy
   ```

## 使用方法

1. Slackワークスペースにボットを招待します。
2. ボットとのDMで「業務開始」と入力するか、ホームタブの「業務開始」ボタンをクリックして勤務を開始します。
3. 「休憩開始」「休憩終了」ボタンで休憩を管理します。
4. 「業務終了」ボタンで勤務を終了し、業務内容を入力します。
5. スケジュール、タスク、休暇申請などの機能はホームタブから利用できます。

## テスト

テストを実行するには以下のコマンドを使用します：

```
pytest
```

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。詳細は[LICENSE](LICENSE)ファイルを参照してください。

# Slack Attendance Management Bot

This Slack bot helps manage employee attendance, including recording work hours, managing break times, setting schedules, managing tasks, and requesting leave.

## Key Features

- Record work start and end times
- Manage break times
- Schedule management
- Task management
- Leave requests
- Generate weekly and monthly reports
- Work pattern analysis

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/your-username/attendance-management-bot.git
   cd attendance-management-bot
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   Create a `.env` file in the project root directory with the following content:
   ```
   BOT_TOKEN=xoxb-your-bot-token
   APP_TOKEN=xapp-your-app-token
   AWS_REGION=us-east-1
   DYNAMODB_ENDPOINT=https://dynamodb.us-east-1.amazonaws.com
   ```

4. Configure AWS CLI:
   ```
   aws configure
   ```

5. Install Serverless Framework:
   ```
   npm install -g serverless
   ```

6. Deploy:
   ```
   serverless deploy
   ```

## Usage

1. Invite the bot to your Slack workspace.
2. Start work by typing "start work" in a DM with the bot or clicking the "Start Work" button in the Home tab.
3. Manage breaks using the "Start Break" and "End Break" buttons.
4. End work using the "End Work" button and enter work content.
5. Access schedule, task, and leave request features from the Home tab.

## Testing

To run tests, use the following command:

```
pytest
```

## License

This project is released under the MIT License. See the [LICENSE](LICENSE) file for details.