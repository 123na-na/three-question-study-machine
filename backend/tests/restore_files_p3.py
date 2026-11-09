"""Part 3: Restore component files and entry ability"""
import os

BASE = r'C:\Users\a\DevEcoStudioProjects\three_question_study_machine\entry\src\main\ets'

def write_file(rel_path, content):
    fp = os.path.join(BASE, rel_path)
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'  Restored: {rel_path}')

# ---- ProgressRing (no Chinese) ----
write_file('component/ProgressRing.ets', """\
@Component
export struct ProgressRing {
  @Prop progress: number = 0;
  @Prop size: number = 80;
  @Prop strokeWidth: number = 8;
  @Prop color: string = '#3B82F6';
  @Prop bgColor: string = '#E2E8F0';
  @Prop showLabel: boolean = true;

  build() {
    Stack() {
      Circle()
        .width(this.size)
        .height(this.size)
        .strokeWidth(this.strokeWidth)
        .stroke(this.bgColor)
        .fill(Color.Transparent)
      Circle()
        .width(this.size)
        .height(this.size)
        .strokeWidth(this.strokeWidth)
        .stroke(this.color)
        .fill(Color.Transparent)
        .strokeLineCap(LineCapStyle.Round)
        .progress({ value: this.progress, total: 100 })
      if (this.showLabel) {
        Text(Math.round(this.progress) + '%')
          .fontSize(this.size * 0.25)
          .fontColor(this.color)
          .fontWeight(FontWeight.Bold)
      }
    }
    .width(this.size)
    .height(this.size)
    .justifyContent(FlexAlign.Center)
    .alignContent(Alignment.Center)
  }
}
""")

# ---- EntryAbility (no Chinese) ----
write_file('entryability/EntryAbility.ets', """\
import { AbilityConstant, UIAbility, Want } from '@kit.AbilityKit';
import { hilog } from '@kit.PerformanceAnalysisKit';
import { window } from '@kit.ArkUI';

export default class EntryAbility extends UIAbility {
  onCreate(want: Want, launchParam: AbilityConstant.LaunchParam): void {
    hilog.info(0x0000, 'testTag', '%{public}s', 'Ability onCreate');
  }

  onDestroy(): void {
    hilog.info(0x0000, 'testTag', '%{public}s', 'Ability onDestroy');
  }

  onWindowStageCreate(windowStage: window.WindowStage): void {
    hilog.info(0x0000, 'testTag', '%{public}s', 'Ability onWindowStageCreate');
    windowStage.loadContent('pages/Index', (err) => {
      if (err.code) {
        hilog.error(0x0000, 'testTag', 'Failed to load the content. Cause: %{public}s', JSON.stringify(err) ?? '');
        return;
      }
      hilog.info(0x0000, 'testTag', 'Succeeded in loading the content.');
    });
  }

  onWindowStageDestroy(): void {
    hilog.info(0x0000, 'testTag', '%{public}s', 'Ability onWindowStageDestroy');
  }

  onForeground(): void {
    hilog.info(0x0000, 'testTag', '%{public}s', 'Ability onForeground');
  }

  onBackground(): void {
    hilog.info(0x0000, 'testTag', '%{public}s', 'Ability onBackground');
  }
}
""")

# ---- EntryBackupAbility (no Chinese) ----
write_file('entrybackupability/EntryBackupAbility.ets', """\
import { BackupExtensionAbility, BundleVersion } from '@kit.CoreFileKit';
import { hilog } from '@kit.PerformanceAnalysisKit';

export default class EntryBackupAbility extends BackupExtensionAbility {
  async onBackup(): Promise<void> {
    hilog.info(0x0000, 'testTag', 'onBackup');
  }

  async onRestore(bundleVersion: BundleVersion): Promise<void> {
    hilog.info(0x0000, 'testTag', 'onRestore');
  }
}
""")

print("Components and EntryAbility restored")
print("Run part 4 for pages")
