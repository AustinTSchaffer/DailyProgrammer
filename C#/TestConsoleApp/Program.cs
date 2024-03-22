// See https://aka.ms/new-console-template for more information

using System.Diagnostics;

internal class Program
{
    // https://learn.microsoft.com/en-us/training/modules/csharp-evaluate-boolean-expressions/6-challenge-2
    static string TestFunc(string permission, int level)
    {
        if (permission == "Admin") {
            if (level > 55) {
                return "Welcome, Super Admin user.";
            } else {
                return "Welcome, Admin user.";
            }
        }

        if (permission == "Manager") {
            if (level >= 20) {
                return "Contact an Admin for access.";
            } else {
                return "You do not have sufficient privileges.";
            }
        }

        return "You do not have sufficient privileges.";
    }

    private static void Main(string[] args)
    {
        var test = "The quick brown whatever etc etc";

        Console.WriteLine(test.Contains("fox"));
        Console.WriteLine(test.Contains("brown"));
        Console.WriteLine(string.Join(", ", test.Split()));

        var coin = new Random();
        var twentyRandomValues = Enumerable.Range(0, 20).Select(i => i * coin.Next(0, 2));
        Console.WriteLine(string.Join(", ", twentyRandomValues));

        var listOfInts = Enumerable.Repeat<List<long>>([1, 2, 3], 5).SelectMany(l => l).ToList();
        foreach (var integer in listOfInts) {
            Console.Write($"{integer} ");
        }
        Console.WriteLine();

        string[] orderIDs = ["B123", "C234", "A345", "C15", "B177", "G3003", "C235", "B179"];
        var filteredIDs = orderIDs.Where(id => id.StartsWith("B"));
        foreach (var id in filteredIDs) {
            Console.WriteLine(id);
        }
    }
}