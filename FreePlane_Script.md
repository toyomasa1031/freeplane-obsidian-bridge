## Freeplaneスクリプト

Freeplaneでタスク属性と期限を設定するスクリプトです。

```groovy
import javax.swing.JOptionPane
import java.time.LocalDate
import java.time.format.DateTimeFormatter

def current = node.attributes.getFirst("task")

if (current == "yes") {

    node.attributes.removeAll("task")
    node.attributes.removeAll("due")

} else {

    def options = ["今日", "明日", "自由入力"] as Object[]

    def choice = JOptionPane.showOptionDialog(
        null,
        "完了予定日を選んでください",
        "タスク期限",
        JOptionPane.DEFAULT_OPTION,
        JOptionPane.PLAIN_MESSAGE,
        null,
        options,
        options[0]
    )

    if (choice == -1) return

    def today = LocalDate.now()
    def dueDate

    if (choice == 0) {

        dueDate = today

    } else if (choice == 1) {

        dueDate = today.plusDays(1)

    } else if (choice == 2) {

        def input = JOptionPane.showInputDialog(
            null,
            "月日を入力してください（例：9/30）",
            "完了予定日",
            JOptionPane.PLAIN_MESSAGE
        )

        if (input == null || !input.trim()) return

        try {

            def parts = input.trim().split("/")

            if (parts.length != 2) {
                throw new Exception()
            }

            def month = parts[0] as int
            def day   = parts[1] as int

            dueDate = LocalDate.of(
                today.year,
                month,
                day
            )

            if (dueDate.isBefore(today)) {
                dueDate = dueDate.plusYears(1)
            }

        } catch (Exception e) {

            JOptionPane.showMessageDialog(
                null,
                "9/30 のように入力してください"
            )

            return
        }
    }

    node.attributes.set("task", "yes")

    def formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd")
    node.attributes.set(
        "due",
        dueDate.format(formatter)
    )
}

// @ExecutionModes({ON_SELECTED_NODE})
```
