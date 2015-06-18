import java.util.Date
import java.text.SimpleDateFormat


object Formatp {
    def main(args: Array[String]) {
        println(strftime("%H:%m:%s '", new Date))
    }

    def strftime(fmt: String, date: Date): String = {
        val java_fmt = new StringBuilder
        val tag = """%[yMdcHhmsl]""".r
        // Escapes normal text as defined by SimpleDateFormat
        def escape(toMatch: String): String = {
          toMatch match {
            case s:String if (!s.isEmpty()) => "'" + s.replaceAll("'", "''") + "'"
            case _ => ""
          }
        }
        var last = 0
        for (m <- tag findAllMatchIn fmt) {
          java_fmt ++= escape(fmt.substring(last, m.start))
          java_fmt ++= (m.matched match {
            case "%y" => "yyyy"
            case "%M" => "MM"
            case "%d" => "dd"
            case "%c" => "a"
            case "%H" => "kk"
            case "%h" => "hh"
            case "%m" => "mm"
            case "%s" => "ss"
            case "%l" => "SSS"
          })
          last = m.end
        }
        java_fmt ++= escape(fmt.substring(last, fmt.length))
        new SimpleDateFormat(java_fmt.toString).format(date)
    }
}
