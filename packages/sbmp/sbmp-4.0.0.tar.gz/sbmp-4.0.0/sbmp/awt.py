string_functions = '''
using System;
public class StringExample
{
    public static void Main(string[] args)
    {
        char[] ch = { 'C', 's', 'h', 'a', 'r', 'p' };
        // String constuctor with array of characters as a parameter
        string str1 = new string(ch);
        Console.WriteLine(str1);
        // string length
        int length = str1.Length;
        Console.WriteLine("Length: " + length);
        string str2 = "Programming";
        // string concatenation
        string joinedString = string.Concat(str1, str2);
        Console.WriteLine("Joined string: " + joinedString);
        Console.WriteLine("Joined string: " + str1+str2);
         // string comparison (equality check)
        Boolean result1 = str1.Equals(str2);
        Console.WriteLine("string str1 and str2 are equal: " + result1);
        // string comparison (dictionary position)
        Console.WriteLine("string str1 and str2 are equal: " + str1.CompareTo(str2));
        string name = "C# Programming";
         // string interpolation
        string message = $"Welcome to {name}";
        Console.WriteLine(message);
        // presence of a character
        int id = name.IndexOf('#');
        Console.WriteLine("The index of #="+id);
        // joining with separator
        Console.Write(string.Join(' ',str1,str2)+"\n");
                String str = "Welcome to C# Programming World";
        String[] spearator = { " " };
        Int32 count = 3; // maximum substring to return
        // split method
        String[] strlist = str.Split(spearator, count,
               StringSplitOptions.RemoveEmptyEntries);
        foreach (String s in strlist)
        {
            Console.WriteLine(s+"\n");
        }
'''

empregfrom_db_connectivity_insert = '''
// file-extension: aspx.cs


using System;
using System.Collections.Generic;
using System.Configuration;
using System.Data.SqlClient;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;
namespace EmpRegDB
{
public partial class EmpRegForm System.Web.UI.Page
{
}
}
protected void Page_Load(object sender, EventArgs e) { }
protected void Button1_Click(object sender, EventArgs e)
{
try
{
SqlConnection conn = new SqlConnection(ConfigurationManager.ConnectionStrings["RegConnectionString"].ConnectionString); conn.Open();
string insertQuery = "insert into emp(name, department, city, salary) values (@name, @department,@city,@salary)"; 
SqlCommand cmd = new SqlCommand(insertQuery, conn); 
cmd.Parameters.AddWithValue("@name", NameTxt.Text);
cmd.Parameters.AddWithValue("@department", DeptTxt.Text);
cmd.Parameters.AddWithValue("@city", CityTxt.Text);
cmd.Parameters.AddWithValue("@salary", SalTxt.Text);
cmd.ExecuteNonQuery();
Response.Write("User registeration done Successfully!!! thank you"); conn.Close();
catch (Exception ex)
}
{
}
}
Response.Write("error" + ex.ToString());

// file-extension: aspx


<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml"> <head runat="server">
<title></title></head>
<body>
<form id="form1" runat="server">
<div>
</div>
<asp:Label ID="Label1" runat="server" Text="Label">Name:</asp:Label>
<asp:TextBox ID="NameTxt" runat="server"></asp:TextBox>
<p>
</p>
<asp:Label ID="Label2" runat="server" Text="Label">Department:</asp:Label> <asp:TextBox ID="DeptTxt" runat="server" Height="25px" Width="151px"></asp:TextBox>
<asp:Label ID="Label3" runat="server" Text="Label">City:</asp:Label>
<asp:TextBox ID="CityTxt" runat="server"></asp:TextBox>
<p>
</p>
<p>
</form>
<asp:Label ID="Label4" runat="server" Text="Label">Salary</asp:Label> <asp:TextBox ID="SalTxt" runat="server"></asp:TextBox>
<asp:Button ID="Button1" runat="server" style="margin-left: 43px" Text="Button" OnClick="Button1_Click"
</body>
</html>
'''

data_grid1 = '''
protected void Button1_Click(object sender, EventArgs e)
        {
            SqlConnection conn = new SqlConnection(ConfigurationManager.ConnectionStrings["ConnectionString"].ConnectionString);
            conn.Open();
            Console.WriteLine("Connection Open ! ");
            string sql = "select * from student";
            SqlCommand cmd = new SqlCommand(sql, conn);
            SqlDataReader sdr = cmd.ExecuteReader();
            Response.Write("ID\tName\tSem\tCity"+"<br>");
            ////Retrieve data from table and Display result
            while (sdr.Read())
            {

                Response.Write(sdr["id"] + "&nbsp;" + sdr["name"]+ "&nbsp; " + sdr["sem"]+ "&nbsp; " + sdr["city"]+"<br>");
                //Console.WriteLine(sdr["name"]);
            }

            conn.Close();
        }
'''

data_grid2 = '''
<html xmlns="http://www.w3.org/1999/xhtml">
<head runat="server">
    <title></title>
</head>
<body>
    <form id="form1" runat="server">
        <div>
        </div>
        <asp:GridView ID="GridView1" runat="server">
        </asp:GridView>
        <asp:Button ID="Button1" runat="server" OnClick="Button1_Click" Text="Button" />
        <asp:SqlDataSource ID="SqlDataSource2" runat="server" ConnectionString="<%$ ConnectionStrings:ConnectionString %>" SelectCommand="SELECT [name], [passwd], [city] FROM [users]"></asp:SqlDataSource>
    </form>
</body>
</html>

protected void Button1_Click(object sender, EventArgs e)
        {
            SqlConnection con = new SqlConnection(ConfigurationManager.ConnectionStrings["ConnectionString"].ConnectionString);

            
                SqlDataAdapter sde = new SqlDataAdapter("Select * from users", con);
                DataSet ds = new DataSet();
                sde.Fill(ds);
                GridView1.DataSource = ds;
                GridView1.DataBind();
         }
 
'''

without_data_grid = '''


        protected void Button1_Click(object sender, EventArgs e)
        {
            SqlConnection conn = new SqlConnection(ConfigurationManager.ConnectionStrings["ConnectionString"].ConnectionString);
            conn.Open();
            Console.WriteLine("Connection Open ! ");
            string sql = "select * from users";
            SqlCommand cmd = new SqlCommand(sql, conn);
            SqlDataReader sdr = cmd.ExecuteReader();

            ////Retrieve data from table and Display result
            while (sdr.Read())
            {
                
                Console.WriteLine(sdr["name"]);
                Response.Write(sdr["name"]);
            }

            conn.Close();
        }
    }
}
'''

file_handling1 = '''
FileStream fo = new FileStream("e:\\file3.txt", FileMode.OpenOrCreate);
StreamWriter sw = new StreamWriter(fo);
Console.WriteLine("Enter the string. null for termination");

while (true)
{
     String str=Console.ReadLine();
    if(string.IsNullOrEmpty(str))
    break;
    sw.WriteLine(str);
}
sw.Flush();
fo.Close();

//

FileStream fi = new FileStream("e:\\file3.txt", FileMode.OpenOrCreate);
StreamReader sr = new StreamReader(fi);
string str1;
Console.WriteLine("The contents of the file are:");
while ((str1 = sr.ReadLine()) != null)
{
   Console.WriteLine(str1);
 }
sr.Close();
fi.Close();
Console.ReadKey();

//

StreamWriter sw = File.AppendText("f:\\file3.txt");
Console.WriteLine("Enter the string. null for termination");

while (true)
{
     String str=Console.ReadLine();
    if(string.IsNullOrEmpty(str))
    break;
    sw.WriteLine(str);
}
sw.Flush();
fo.Close();

//

 FileStream fi = new FileStream("e:\\bird.jpg", FileMode.OpenOrCreate);
 FileStream fo = new FileStream("e:\\MyDir1\\bird.jpg",        FileMode.OpenOrCreate);
 int i;
 while ((i = fi.ReadByte()) != -1)
 {
     fo.WriteByte((byte)i);
 }
 fi.Close();
 fo.Close();
 Console.ReadKey();

 //

  using(TextWriter tw = File.CreateText("e:\\file.txt"))
       {
           tw.WriteLine("C# File Handling");
           tw.WriteLine("TextReader Class and TextWriter Class");
        }
 using (TextReader tr = File.OpenText("e:\\file.txt"))
        {
                Console.WriteLine(tr.ReadToEnd());
        }
        Console.ReadKey();

        
//


// only event handling code
private void button2_Click(object sender, EventArgs e)
{
int num1=Convert.ToInt32(textBox1.Text);
int
num2=Convert.ToInt32(textBox2.Text);
int sum=num1+ num2;
textBox3. Text=sum.ToString();
}

'''

validators = '''
function chkEmail()
             {
                 var email = document.getElementById("<%= EmailID.ClientID %>").value;
                 var emailExp = /^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([com\co\.\in])+$/; 

                 if (!email.match(emailExp))
                  {
                     alert("Invalid Email Id");
                     return false;
                 }
             }

             
<asp:RequiredFieldValidator ID="someUniqueId"
runat="server" ControlToValidate ="someUniqueControlId"
ErrorMessage="ErrorToDisplayOnValidationFailure"
InitialValue="aPlaceholderValue">
</asp:RequiredFieldValidator>

<asp:RangeValidator ID="some unique id"
runat="server" ControlToValidate ="someUniqueControlId"
ErrorMessage="ErrorToDisplayOnValidationFailure"
Type="Integer" MinimumValue=”0” MaximumValue=”100”>
</asp:RangeValidator>

<asp:RegularExpressionValidator ID="someUniqueId"
runat="server" ControlToValidate ="someUniqueControlId"
ErrorMessage="ErrorToDisplayOnValidationFailure"
ValidationExpression=”aRegexPattern”>
</asp:RegularExpressionValidator>

<asp:CompareValidator ID="someUniqueId"
runat="server" ControlToValidate ="someUniqueControlId"
ErrorMessage="ErrorToDisplayOnValidationFailure"
Type="string" ControlToCompare=”ControlToValidateIdOfAnotherControl”
ValueToCompare=”aFixedValue” Operator=”Equal”>
</asp:CompareValidator>

<asp:CustomValidator ID="someUniqueId"
runat="server" ControlToValidate ="someUniqueControlId"
ErrorMessage="ErrorToDisplayOnValidationFailure"
ClientValidationFunction=”functionName”>
</asp:CustomValidator>

<asp:ValidationSummary ID="ValidationSummaryControl"
runat="server" DisplayMode=”BulletList” ShowSummary=”true”
HeaderText=”List of Errors” />
'''

validators2 = '''
<%@ Page Language="C#" AutoEventWireup="true" CodeBehind="Validators.aspx.cs" Inherits="WebApplication1.WebForm2" %>

<!DOCTYPE html>

<html xmlns="http://www.w3.org/1999/xhtml">
<head runat="server">
    <title></title>
</head>
<body>
    <form id="form1" runat="server">

   <table style="width: 66%;">
   
      <tr>
         <td class="style1" colspan="3" align="center">
         <asp:Label ID="lblmsg" 
            Text="President Election Form : Choose your president" 
            runat="server" />
         </td>
      </tr>

      <tr>
         <td class="style3">
            Candidate:
         </td>

         <td class="style2">
            <asp:DropDownList ID="ddlcandidate" runat="server"  style="width:239px">
               <asp:ListItem>Please choose a candidate</asp:ListItem>
               <asp:ListItem>M H Kabir</asp:ListItem>
               <asp:ListItem>Steve Taylor</asp:ListItem>
               <asp:ListItem>John Abraham</asp:ListItem>
               <asp:ListItem>Venus Williams</asp:ListItem>
            </asp:DropDownList>
         </td>
          <td>
            <asp:RequiredFieldValidator ID="rfvcandidate" 
               runat="server" ControlToValidate ="ddlcandidate" 
               InitialValue="Please choose a candidate"
               ErrorMessage="Please choose a candidate"
               ForeColor="Red">
            </asp:RequiredFieldValidator>
         </td>
      </tr>

      <tr>
         <td class="style3">
            House:
         </td>

         <td class="style2">
            <asp:RadioButtonList ID="rblhouse" runat="server" RepeatLayout="Flow">
               <asp:ListItem>Red</asp:ListItem>
               <asp:ListItem>Blue</asp:ListItem>
               <asp:ListItem>Yellow</asp:ListItem>
               <asp:ListItem>Green</asp:ListItem>
            </asp:RadioButtonList>
         </td>
          <td>
            <asp:RequiredFieldValidator ID="rfvhouse" runat="server" 
               ControlToValidate="rblhouse" ErrorMessage="Enter your house name" ForeColor="Red" >
            </asp:RequiredFieldValidator>
            <br />
         </td>
      </tr>

      <tr>
         <td class="style3">
            Class:
         </td>

         <td class="style2">
            <asp:TextBox ID="txtclass" runat="server"></asp:TextBox>
         </td>

         <td>
            <asp:RangeValidator ID="rvclass" 
               runat="server" ControlToValidate="txtclass" 
               ErrorMessage="Enter your class (6 - 12)" MaximumValue="12" 
               MinimumValue="6" Type="Integer" ForeColor="Red">
            </asp:RangeValidator>
         </td>
      </tr>
       <tr>
         <td class="style3">
            Email:
         </td>

         <td class="style2">
            <asp:TextBox ID="txtemail" runat="server" style="width:250px">
            </asp:TextBox>
         </td>

         <td>
            <asp:RegularExpressionValidator ID="remail" runat="server" 
               ControlToValidate="txtemail" ErrorMessage="Enter your email" 
               ForeColor="Red" ValidationExpression="\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*"> 
            </asp:RegularExpressionValidator>
         </td>
      </tr>

      <tr>
         <td class="style3" align="center" colspan="3">
            <asp:Button ID="BtnSubmit" runat="server" onclick="BtnSubmit_Click" 
               style="text-align: center" Text="Submit"  />
         </td>
      </tr>
   </table>
   <asp:ValidationSummary ID="ValidationSummary1" runat="server" 
      DisplayMode ="BulletList" ShowSummary ="true" HeaderText="Errors:" ForeColor="Red" />
</form>
</body>
</html>
'''

validators3 = '''
<%@ Page Language="C#" AutoEventWireup="true" CodeFile="Default.aspx.cs" Inherits=“namespace._Default" %>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head runat="server">
    <title>Untitled Page</title>
</head>
<body>
    <form id="form1" runat="server">
    <div>
        <asp:Label ID="Label3" runat="server" Style="top: 241px; left: 70px; position: absolute;
            height: 22px; width: 128px; bottom: 282px;" Text="Enter your email id:"></asp:Label>
        <asp:Label ID="Label1" runat="server" Style="top: 54px; left: 74px; position: absolute;
            height: 22px; width: 128px" Text="Enter your name:"></asp:Label>
        <asp:TextBox ID="TextBox1" runat="server" Style="top: 54px; left: 221px; position: absolute;
            height: 22px; width: 128px; right: 396px;"></asp:TextBox>
        <asp:RequiredFieldValidator ID="RequiredFieldValidator1" runat="server" Style="top: 56px;
            left: 378px; position: absolute; height: 22px; width: 128px" ErrorMessage="RequiredFieldValidator"
            ControlToValidate="TextBox1">name is
        mandatory </asp:RequiredFieldValidator>
    </div>
    <p>
        <asp:Button ID="Button1" runat="server" Style="top: 311px; left: 267px; position: absolute;
            height: 26px; width: 61px" Text="Submit" />
    </p>
    <asp:TextBox ID="TextBox3" runat="server" Style="top: 145px; left: 217px; position: absolute;
        height: 22px; width: 131px" TextMode="Password"></asp:TextBox>
    <p>
        <asp:TextBox ID="TextBox2" runat="server" Style="top: 101px; left: 218px; position: absolute;
            height: 22px; width: 131px" TextMode="Password"></asp:TextBox>
        <asp:Label ID="Label4" runat="server" Style="top: 105px; left: 74px; position: absolute;
            height: 22px; width: 128px" Text="Password"></asp:Label>
        <asp:TextBox ID="TextBox5" runat="server" Style="top: 239px; left: 210px; position: absolute;
            height: 22px; width: 134px"></asp:TextBox>
    </p>
    <asp:RequiredFieldValidator ID="RequiredFieldValidator3" runat="server" Style="top: 98px;
        left: 367px; position: absolute; height: 26px; width: 162px" ErrorMessage="password required"
        ControlToValidate="TextBox2"></asp:RequiredFieldValidator>
    <asp:RequiredFieldValidator ID="RequiredFieldValidator2" runat="server" Style="top: 145px;
        left: 367px; position: absolute; height: 26px; width: 162px" ErrorMessage="password required"
        ControlToValidate="TextBox3"></asp:RequiredFieldValidator>
    <asp:CompareValidator ID="CompareValidator1" runat="server" Style="top: 149px; left: 512px;
        position: absolute; height: 26px; width: 162px" ErrorMessage="CompareValidator"
        ControlToValidate="TextBox3" ValueToCompare="hello"></asp:CompareValidator>
        <p>
        <asp:Label ID="Label5" runat="server" Style="top: 148px; left: 71px; position: absolute;
            height: 22px; width: 128px; bottom: 375px;" Text="Confirm Password"></asp:Label>
        <asp:TextBox ID="TextBox4" runat="server" Style="top: 194px; left: 212px; position: absolute;
            height: 22px; width: 140px"></asp:TextBox>
        <asp:Label ID="Label6" runat="server" Style="top: 194px; left: 71px; position: absolute;
            height: 22px; width: 128px; bottom: 329px;" Text="Enter your age:"></asp:Label>
    </p>
    <asp:RangeValidator ID="RangeValidator1" runat="server" Style="top: 194px; left: 365px;
        position: absolute; height: 22px; width: 105px" ErrorMessage="RangeValidator"
        ControlToValidate="TextBox4" MaximumValue="100" MinimumValue="18" Type="Integer"></asp:RangeValidator>
    <asp:RegularExpressionValidator ID="RegularExpressionValidator1" runat="server" Style="top: 234px;
        left: 366px; position: absolute; height: 22px; width: 177px"
        ErrorMessage="RegularExpressionValidator" ControlToValidate="TextBox5"
        ValidationExpression="\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*"></asp:RegularExpressionValidator>
    </form>
</body>
</html>
'''

validators4 = '''
<%@ Page Language="C#" AutoEventWireup="true" CodeBehind="CustomValidator.aspx.cs" Inherits="WebApplication1.CustomValidator" %>

<!DOCTYPE html>

<html xmlns="http://www.w3.org/1999/xhtml">
<head runat="server">
    <title></title>
</head>
<body>
    <form id="form1" runat="server">
    <div>
        <asp:Label ID="Label1" runat="server" Text="User ID:"></asp:Label>
 <asp:TextBox ID="TextBox1" runat="server"></asp:TextBox>
 <asp:RequiredFieldValidator ID="RequiredFieldValidator1" runat="server"
            ControlToValidate="TextBox1" ErrorMessage="User id required"></asp:RequiredFieldValidator>

        <asp:CustomValidator ID="CustomValidator1" runat="server" OnServerValidate="UserCustomValidate"
            ControlToValidate="TextBox1"
            ErrorMessage="User ID should have atleast a capital, small and digit and should be greater than 5 and less
than 26 letters"
            SetFocusOnError="True"></asp:CustomValidator>
        </div>
    <asp:Button ID="Button1" runat="server" OnClick="Button1_Click" Text="Submit"></asp:Button>
    </form>
</body>
</html>

 protected void UserCustomValidate(object source, ServerValidateEventArgs args)
        {
            string str = args.Value;
            args.IsValid = false;
            //checking for input length greater than 6 and less than 25 characters
            if (str.Length < 6 || str.Length > 25)
            {
                return;
            }
            //checking for a atleast a single capital letter
            bool capital = false;
            foreach (char ch in str)
            {
                if (ch >= 'A' && ch <= 'Z')
                {
                    capital = true;
                    break;
                }
            }
            if (!capital)
            {
                return;
            }
 //checking for a atleast a single lower letter
            bool lower = false;
            foreach (char ch in str)
            {
                if (ch >= 'a' && ch <= 'z')
                {
                    lower = true;
                    break;
                }
            }
            if (!lower)
            {
                return;
            }
            bool digit = false;
            foreach (char ch in str)
            {
                if (ch >= '0' && ch <= '9')
                {
                    digit = true;
                    break;
                }
            }
            if (!digit)
            {
                return;
            }
            args.IsValid = true;
        } //end of UserCustomValidate method
'''

awt_codes = {
    "string_functions.txt": string_functions,
    "empregfrom_db_connectivity_insert.txt": empregfrom_db_connectivity_insert,
    "data_grid1.txt": data_grid1,
    "data_grid2.txt": data_grid2,
    "without_data_grid.txt": without_data_grid,
    "file_handling1.txt": file_handling1,
    "validators.txt": validators,
    "validators2.txt": validators2,
    "validators3.txt": validators3,
    "validators4.txt": validators4
}

def awtcodes_():
    for file,code in awt_codes.items():
        print(file)
    filename = input("Enter filename: ")
    with open(filename, 'w') as f:
        f.write(awt_codes[filename])