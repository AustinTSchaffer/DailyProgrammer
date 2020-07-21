import java.util.ArrayList;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.io.FileOutputStream;
import java.io.PrintStream;

public class Main {

    public static void main(String[] args) {

		try {
			System.setOut(new PrintStream(new FileOutputStream("../Printout from Main.java.txt")));	
		} catch(Exception e) {
			System.setOut(System.out);
		}

        excelChallenge();
		sinusChallenge();
        kiosChallenge1();
		kiosChallenge2();
		htmlNestingChallenge();
		yoloTtlChallenge1();
		yoloTtlChallenge2();

    }
	
	public static void excelChallenge() {
		System.out.println("/// -----------------------------------");
        System.out.println("/// Excel-lent! Challenge Demonstration");
        System.out.println("/// -----------------------------------");
        
        
        System.out.println(ExcellentParser.parse("R1C1"));
        System.out.println(ExcellentParser.parse("R3C1"));
        System.out.println(ExcellentParser.parse("R1C3"));
        System.out.println(ExcellentParser.parse("R299999999C26"));
        System.out.println(ExcellentParser.parse("R52C52"));
        System.out.println(ExcellentParser.parse("R53C17576"));
        System.out.println(ExcellentParser.parse("R53C17602"));
        System.out.println(ExcellentParser.parse("R0C0"));   
	}
	
	public static void sinusChallenge() {
		System.out.println("/// ------------------------------------");
		System.out.println("/// Sinus Rhythm Challenge Demonstration");
		System.out.println("/// ------------------------------------");
		
		
		String graph = new SinusRhythmPlotter()
			.addWave(1, "---------------------------------")
			.addWave(6, "+++++++++++++++++++++++++++++++")
			.addWave(0, "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
			.addWave(-3, "@@@@@@@@@@@@@@@@@@@@")
			.build().toString();
		System.out.println(graph);
		

		System.out.println(
				new SinusRhythmPlotter()
				.addWave(4, "ThisClassCanAlsoBeUsedToGenerateRailFenceCiphers")
				.build().toString()
				);
	}

	public static void kiosChallenge1() {
		System.out.println("/// -----------------------------------------------");
        System.out.println("/// Kickin' it Old School Challenge Demonstration 1");
        System.out.println("/// -----------------------------------------------");
        
        
        ArrayList<String> challenge1 = new NumpadWordMatcher()
                .addDictionaryEntry("QQ")
                .addKeyStroke("27")
                .execute();
        
        for (String s : challenge1) {
            System.out.println(s);
        }
	}
	
	public static void kiosChallenge2() {
		System.out.println("/// -----------------------------------------------");
        System.out.println("/// Kickin' it Old School Challenge Demonstration 2");
        System.out.println("/// -----------------------------------------------");

        ArrayList<String> challenge2 = new NumpadWordMatcher()
                .addDictionaryEntry("JOVE")
                .addDictionaryEntry("CLOVE")
                .addDictionaryEntry("BAD")
                .addDictionaryEntry("LOUD")
                .addDictionaryEntry("LOUD")
                .addDictionaryEntry("GLOVE")
                .addKeyStroke("5683")
                .addKeyStroke("223")
                .execute();
        
        for (String s : challenge2) {
            System.out.println(s);
        }
	}

	public static void htmlNestingChallenge() {
		System.out.println("/// ---------------------------------------");
        System.out.println("/// HTML Tag Matching and Nesting Challenge");
        System.out.println("/// ---------------------------------------");

        System.out.println(ProperNestingVerifier.verify("The following text<C><B>is centered and in boldface</B></C>#"));
        System.out.println(ProperNestingVerifier.verify("<B>This <\\g>is <B>boldface</B> in <<*> a</B> <\\6> <<d>sentence#"));
        System.out.println(ProperNestingVerifier.verify("<B><C> This should be centered and in boldface, but the tags are wrongly nested </B></C>#"));
        System.out.println(ProperNestingVerifier.verify("<B>This should be in boldface, but there is an extra closing <img src='tag.gif'>tag</B></C>#"));
        System.out.println(ProperNestingVerifier.verify("<B><C>This should be centered and in boldface, but there is a missing closing tag</C>#"));
        System.out.println(ProperNestingVerifier.verify("#"));
	}	

	public static void yoloTtlChallenge1() {
		System.out.println("/// -----------------------------------");
        System.out.println("/// YOLO TTL Network Sample 1 Challenge");
        System.out.println("/// -----------------------------------");

		YOLOTTL yolottl = new YOLOTTL()
				.addConnection(10, 15)
				.addConnection(15, 20)
				.addConnection(20, 25)
				.addConnection(10, 30)
				.addConnection(30, 47)
				.addConnection(47, 50)
				.addConnection(25, 45)
				.addConnection(45, 65)
				.addConnection(15, 35)
				.addConnection(35, 55)
				.addConnection(20, 40)
				.addConnection(50, 55)
				.addConnection(35, 40)
				.addConnection(55, 60)
				.addConnection(40, 60)
				.addConnection(60, 65);

		System.out.println(yolottl.testPacket(35, 2));
		System.out.println(yolottl.testPacket(35, 3));

	}

	public static void yoloTtlChallenge2() {
		System.out.println("/// -----------------------------------");
        System.out.println("/// YOLO TTL Network Sample 2 Challenge");
        System.out.println("/// -----------------------------------");

		YOLOTTL yolottl = new YOLOTTL()
				.addConnection(1,2)
				.addConnection(1,3)
				.addConnection(2,7)
				.addConnection(3,4)
				.addConnection(3,5)
				.addConnection(4,6)
				.addConnection(5,10)
				.addConnection(5,11)
				.addConnection(6,11)
				.addConnection(7,6)
				.addConnection(7,8)
				.addConnection(7,9)
				.addConnection(8,9)
				.addConnection(8,6);
				

		System.out.println(yolottl.testPacket(1,1));
		System.out.println(yolottl.testPacket(1,2));
		System.out.println(yolottl.testPacket(3,2));
		System.out.println(yolottl.testPacket(3,3));
	}
}
