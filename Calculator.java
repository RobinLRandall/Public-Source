/*
Name: Hemanth. B,  Robin Randall
Website: http://www.java-swing-tutorial.com

Topic: A basic Java Swing Calculator

Conventions Used in Source code
---------------------------------
	1. All JLabel components start with jlb*
	2. All JPanel components start with jpl*
	3. All JMenu components start with jmenu*
	4. All JMenuItem components start with jmenuItem*
	5. All JDialog components start with jdlg*
	6. All JButton components start with jbn*
*/

import java.awt.BorderLayout;
import java.awt.Color;
//import java.awt.Container;
import java.awt.FlowLayout;
import java.awt.Font;
import java.awt.GridLayout;
import java.awt.Window;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.KeyEvent;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;

import javax.swing.JButton;
import javax.swing.JDialog;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JMenu;
import javax.swing.JMenuBar;
import javax.swing.JMenuItem;
import javax.swing.JPanel;
import javax.swing.JTextArea;
import javax.swing.KeyStroke;

public class Calculator extends JFrame implements ActionListener{
	private static final long serialVersionUID = 1L; 
	// Variables
	final int MAX_INPUT_LENGTH = 20;
	final int INPUT_MODE = 0;
	final int RESULT_MODE = 1;
	final int ERROR_MODE = 2;
	int displayMode;
    int fixDigits =15;
	boolean clearOnNextDigit, percent;
	double lastNumber;
	String lastOperator;

	private JMenu jmenuFile, jmenuHelp;
	private JMenuItem jmenuitemExit, jmenuitemAbout;
	

	private JLabel jlbOutput, jlbOutput0;
	private JButton jbnButtons[];
	private JPanel jplMaster, jplBackSpace, jplControl;
	
	/*
	 * Font(String name, int style, int size)
      Creates a new Font from the specified name, style and point size.
	 */
	
	Font f12 =  new Font("Verdana", 0, 12);
	Font f121 = new Font("Verdana", 1, 12);
	Font f20 =  new Font("Verdana", 2, 20);
	
	
	// Constructor 
	public Calculator() 
	{
		/* Set Up the JMenuBar.
		 * Have Provided All JMenu's with Mnemonics
		 * Have Provided some JMenuItem components with Keyboard Accelerators
		 */ 
		
		jmenuFile = new JMenu("File");
		jmenuFile.setFont(f121);
		jmenuFile.setMnemonic(KeyEvent.VK_F);
		
		jmenuitemExit = new JMenuItem("Exit");
		jmenuitemExit.setFont(f12);
		jmenuitemExit.setAccelerator(KeyStroke.getKeyStroke( KeyEvent.VK_X, 
													ActionEvent.CTRL_MASK));
		jmenuFile.add(jmenuitemExit);

		jmenuHelp = new JMenu("Help");
		jmenuHelp.setFont(f121);
		jmenuHelp.setMnemonic(KeyEvent.VK_H);

		jmenuitemAbout = new JMenuItem("About Calculator");
		jmenuitemAbout.setFont(f12);
		jmenuHelp.add(jmenuitemAbout);
		
		JMenuBar mb = new JMenuBar();
		mb.add(jmenuFile);
		mb.add(jmenuHelp);
		setJMenuBar(mb);
		
		//Set frame layout manager

		setBackground(Color.gray);

		jplMaster = new JPanel();

		jlbOutput = new JLabel("0");
		jlbOutput.setFont(f20);
		jlbOutput.setHorizontalTextPosition(JLabel.RIGHT);
		jlbOutput.setBackground(Color.WHITE);
		jlbOutput.setOpaque(true);
		
		jlbOutput0 = new JLabel(" ");
		jlbOutput0.setFont(f12);
		jlbOutput0.setHorizontalTextPosition(JLabel.RIGHT);
		jlbOutput0.setBackground(Color.WHITE);
		jlbOutput0.setOpaque(true);
		
		// Add components to frame
		getContentPane().add(jlbOutput0, BorderLayout.NORTH);
		getContentPane().add(jlbOutput);

		jbnButtons = new JButton[32]; //  Gives max number of buttons

//		GridLayout(int rows, int cols, int hgap, int vgap) 

		JPanel jplButtons = new JPanel();			// container for Jbuttons
		
     
		// Create numeric Jbuttons
		for (int i=0; i<=9; i++)
		{
			// set each Jbutton label to the value of index
			jbnButtons[i] = new JButton(String.valueOf(i));
		}

		// Create operator Jbuttons
		jbnButtons[10] = new JButton("+/-");
		jbnButtons[11] = new JButton(".");
		//
		jbnButtons[13] = new JButton("/");
		jbnButtons[14] = new JButton("*");
		jbnButtons[15] = new JButton("-");
		jbnButtons[16] = new JButton("+");
		//
		jbnButtons[17] = new JButton("sqrt");
		jbnButtons[18] = new JButton("1/x");
		jbnButtons[19] = new JButton("%");
		jbnButtons[12] = new JButton("=");
		
		jplBackSpace = new JPanel();
		jplBackSpace.setLayout(new GridLayout(1, 1, 2, 2));

		jbnButtons[20] = new JButton("Backspace");
		jplBackSpace.add(jbnButtons[20]);

		jplControl = new JPanel();
		jplControl.setLayout(new GridLayout(1, 2, 2 ,2));

		jbnButtons[21] = new JButton("CE");
		jbnButtons[22] = new JButton("C");

		jbnButtons[23] = new JButton("x^2");
		jbnButtons[24] = new JButton("x^y");
		jbnButtons[25] = new JButton("log x");
		jbnButtons[26] = new JButton("ln x");
		
		jbnButtons[27] = new JButton("n!");
		jbnButtons[28] = new JButton("y rt x");
		jbnButtons[29] = new JButton("Mod");
		jbnButtons[30] = new JButton("pi");
		jbnButtons[31] = new JButton("fix");
		
		jplControl.add(jbnButtons[31]); // fix
		jplControl.add(jbnButtons[21]); // CE
		jplControl.add(jbnButtons[22]); // C
//		Setting all Numbered JButton's to Blue. The rest to Red
		for (int i=0; i<jbnButtons.length; i++)	{
			jbnButtons[i].setFont(f12);
			
			if (i<10)
				jbnButtons[i].setForeground(Color.blue);
			else
				jbnButtons[i].setForeground(Color.red);
		}
		jbnButtons[11].setFont(f20);  //  "dot" gets better notice
		jbnButtons[12].setFont(f20);  //  "=" should stand out

		// Set panel layout manager for a 4 by 5 grid
		jplButtons.setLayout(new GridLayout(4, 6, 2, 2));
		//Add buttons to keypad panel starting at top left
		// First row
		for(int i=7; i<=9; i++)		{
			jplButtons.add(jbnButtons[i]);
		}
		
		// add button / and sqrt  x^2  n!
		jplButtons.add(jbnButtons[13]);
		jplButtons.add(jbnButtons[17]);
		jplButtons.add(jbnButtons[23]);
		jplButtons.add(jbnButtons[27]);
		// Second row
		for(int i=4; i<=6; i++)
		{
			jplButtons.add(jbnButtons[i]);
		}
		
		// add button * and 1/x  x^y   y rt x
		jplButtons.add(jbnButtons[14]);
		jplButtons.add(jbnButtons[18]);
		jplButtons.add(jbnButtons[24]);
		jplButtons.add(jbnButtons[28]);
		// Third row
		for( int i=1; i<=3; i++)
		{
			jplButtons.add(jbnButtons[i]);
		}
		
		//adds button - and %  log x  Mod
		jplButtons.add(jbnButtons[15]);
		jplButtons.add(jbnButtons[19]);
		jplButtons.add(jbnButtons[25]);
		jplButtons.add(jbnButtons[29]);
		
		//Fourth Row
		// add 0, +/-, ., +, and =  ln x pi
		jplButtons.add(jbnButtons[10]);
		jplButtons.add(jbnButtons[0]);
		jplButtons.add(jbnButtons[11]);
		jplButtons.add(jbnButtons[16]);
		jplButtons.add(jbnButtons[12]);
		jplButtons.add(jbnButtons[26]);
		jplButtons.add(jbnButtons[30]);

		jplMaster.setLayout(new BorderLayout());
		jplMaster.add(jplBackSpace, BorderLayout.WEST);
		jplMaster.add(jplControl, BorderLayout.EAST);
		jplMaster.add(jplButtons, BorderLayout.SOUTH);

		// Add components to frame
		getContentPane().add(jplMaster, BorderLayout.SOUTH);
		requestFocus();
		
		//activate ActionListener
		for (int i=0; i<jbnButtons.length; i++){
			jbnButtons[i].addActionListener(this);
		}
		
		jmenuitemAbout.addActionListener(this);
		jmenuitemExit.addActionListener(this);

		clearAll();

		//add WindowListener for closing frame and ending program
		addWindowListener(new WindowAdapter() {

				public void windowClosed(WindowEvent e)
				{
					System.exit(0);
				}
			}
		);
		this.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
	}	//End of Contructor Calculator

	// Perform action
	public void actionPerformed(ActionEvent e){
		double result = 0;
	   
		if(e.getSource() == jmenuitemAbout){
			JDialog dlgAbout = new CustomABOUTDialog(this, "About Java Swing Calculator", true);
			dlgAbout.setFont(f12);
			dlgAbout.setVisible(true);
		}else if(e.getSource() == jmenuitemExit){
			System.exit(0);
		}	

		// Search for the button pressed until end of array or key found
		for (int i=0; i<jbnButtons.length; i++)
		{
			if(e.getSource() == jbnButtons[i])
			{
				switch(i)
				{
					case 0:
						addDigitToDisplay(i);
						break;

					case 1:
						addDigitToDisplay(i);
						break;

					case 2:
						addDigitToDisplay(i);
						break;

					case 3:
						addDigitToDisplay(i);
						break;

					case 4:
						addDigitToDisplay(i);
						break;

					case 5:
						addDigitToDisplay(i);
						break;

					case 6:
						addDigitToDisplay(i);
						break;

					case 7:
						addDigitToDisplay(i);
						break;

					case 8:
						addDigitToDisplay(i);
						break;

					case 9:
						addDigitToDisplay(i);
						break;

					case 10:	// +/-
						processSignChange();
						setDisplayString0(getDisplayString0()+"+/-");
						break;

					case 11:	// decimal point
						addDecimalPoint();
						setDisplayString0(getDisplayString0()+".");								
						break;

					case 12:	// =
						processEquals();
						setDisplayString0(getDisplayString0()+"=");		
						break;

					case 13:	// divide
						processOperator("/");
						break;

					case 14:	// *
						processOperator("*");
						break;

					case 15:	// -
						processOperator("-");
						break;

					case 16:	// +
						processOperator("+");
						break;

					case 17:	// sqrt
						if (displayMode != ERROR_MODE)
						{
							try
							{  if (displayMode == INPUT_MODE){
								if (getDisplayString().indexOf("-") == 0){
									displayError("Invalid input for function!");
								}
								result = Math.sqrt(getNumberInDisplay());
								displayResult(result);
								
							    }else if (displayMode == RESULT_MODE){
								result = Math.sqrt(getNumberInDisplay());
								displayResult(result);
						     	}
							setDisplayString0(getDisplayString0() + "sqrt");
							}
							catch(Exception ex)
							{
								displayError("Invalid input for function!");
								displayMode = ERROR_MODE;
							}
						}
						break;

					case 18:	// 1/x
						if (displayMode != ERROR_MODE){
							try
							{   if (displayMode == INPUT_MODE){
								  if (getNumberInDisplay() == 0){
									displayError("Cannot divide by zero!");
								  }
								result = 1 / getNumberInDisplay();
								setDisplayString(Double.toString(result));
								displayResult(result);
								
							    }else if (displayMode == RESULT_MODE){
								result = 1 / getNumberInDisplay();
								displayResult(result);
							    }
							setDisplayString0(getDisplayString0() + "1/x");
							}
							
							catch(Exception ex)	{
								displayError("Cannot divide by zero!");
								displayMode = ERROR_MODE;
							}
						}
						break;

					case 19:	// %  (This for Percent, NOT Mod function)
						if (displayMode != ERROR_MODE){
							if (displayMode == INPUT_MODE) {
							    result = (double) getNumberInDisplay() / 100;
							    setDisplayString(Double.toString(result));
							    displayResult(result);
							}
						    else if (displayMode == RESULT_MODE){
						    result = (double) getNumberInDisplay() / 100;
						    displayResult(result);
						    }
							setDisplayString0(getDisplayString0() + "%");
						}
						break;

					case 20:	// backspace
						if (displayMode != ERROR_MODE){
							setDisplayString(getDisplayString().substring(0,
										getDisplayString().length() - 1));
							setDisplayString0(getDisplayString0().substring(0,
									getDisplayString0().length() - 1));
							
							if (getDisplayString().length() < 1)
								setDisplayString("0");
						}
						break;

					case 21:	// CE
						clearExisting();
						break;

					case 22:	// C
						clearAll();
						break;
					case 23:    //  x^2
						if (displayMode != ERROR_MODE){
							if (displayMode == INPUT_MODE) {
							    double x = (double) getNumberInDisplay();
							    result = (double) Math.pow(x, 2.0);
							    setDisplayString(Double.toString(result));
							    displayResult(result);
							}
						    else if (displayMode == RESULT_MODE){
						    double x = (double) getNumberInDisplay();
						    result = (double) Math.pow(x, 2.0);
						    displayResult(result);
						    }
							setDisplayString0(getDisplayString0() + "x^2");
						}
						break;

					case 24: //  x^y
						processOperator("x^y");
						break;

					case 25: // log x
						if (displayMode != ERROR_MODE){
							if (displayMode == INPUT_MODE) {
							    double x = (double) getNumberInDisplay();
							    result = (double) Math.log10(x);
							    setDisplayString(Double.toString(result));
							    displayResult(result);
							}
						    else if (displayMode == RESULT_MODE){
						    double x = (double) getNumberInDisplay();
						    result = (double) Math.log10(x);
						    displayResult(result);
						    }
							setDisplayString0(getDisplayString0() + "log x");
						}
						break;

					case 26: //  ln x
						if (displayMode != ERROR_MODE){
							if (displayMode == INPUT_MODE) {
							    double x = (double) getNumberInDisplay();
							    result = (double) Math.log(x);
							    setDisplayString(Double.toString(result));
							    displayResult(result);
							}
						    else if (displayMode == RESULT_MODE){
						    double x = (double) getNumberInDisplay();
						    result = (double) Math.log(x);
						    displayResult(result);
						    }
							setDisplayString0(getDisplayString0() + "ln x");
						}
						break;

					case 27: //   n!
						
						if (displayMode != ERROR_MODE)
						{
							try
							{
								if (getNumberInDisplay() > 700) // 720! gives "infinity" as answer
									displayError("Answer too large to display!");
								
								if (getDisplayString().indexOf("-") == 0) 
									displayError("Invalid input for function!");
								
								int g = (int)getNumberInDisplay();
								result = 1;
								for ( int f = 1; f <= g ; f++ )  {
								            result *= f;
								    }
								displayResult(result);
								setDisplayString0(getDisplayString0() + "n!");
							}
							catch(Exception ex)
							{
								displayError("Answer too large to display!");
								displayMode = ERROR_MODE;
							}
						}
						break;

					case 28: //  y rt x
						if (displayMode != ERROR_MODE)
						{
							try
							{
								if ((getDisplayString().indexOf("-") == 0)
								    || (lastNumber < 0)) {
									displayError("Invalid input for function!");
								}
								processOperator("y rt x");
							}
							catch(Exception ex)
							{
								displayError("Invalid input for function!");
								displayMode = ERROR_MODE;
							}
						}
						break;

					case 29:    // Mod
						processOperator("Mod");
						break;

					case 30:	// pi
						if (displayMode != ERROR_MODE){
							
						  try {	
							if (displayMode == INPUT_MODE) {
								result = 3.1415926535897932384626433832795;
							    setDisplayString(Double.toString(result));
							    displayResult(result);
							}
						    else if (displayMode == RESULT_MODE){
							    result = 3.1415926535897932384626433832795;
						        displayResult(result);
						    }
						    setDisplayString0(getDisplayString0() + "pi");
					    }catch(Exception ex)
							{
							displayError("Invalid!");
							displayMode = ERROR_MODE;
						}
					}
						break;
						
					case 31:	// fix
						if (displayMode != ERROR_MODE){
							if (displayMode == INPUT_MODE) {
								fixDigits = (int)getNumberInDisplay();
							    setDisplayString(getDisplayString());
							}
						    else if (displayMode == RESULT_MODE){
								fixDigits = (int)getNumberInDisplay();
						        setDisplayString(getDisplayString());
						    }
							setDisplayString0(getDisplayString0() + "fix" );
						}
						break;

				}
			}
		}
	}

	void setDisplayString(String s){
		jlbOutput.setText(s);
	}
	void setDisplayString0(String s){
		jlbOutput0.setText(s);
	}
	String getDisplayString (){
		return jlbOutput.getText();
	}
	String getDisplayString0 (){
		return jlbOutput0.getText();
	}
	void addDigitToDisplay(int digit){
		if (clearOnNextDigit)
			setDisplayString("");

		String inputString = getDisplayString();
		String inputString0 = getDisplayString0();
		
		if (inputString.indexOf("0") == 0){
			inputString = inputString.substring(1);
		}

		if ((!inputString.equals("0") || digit > 0)  && inputString.length() < MAX_INPUT_LENGTH){
			setDisplayString(inputString + digit);
			setDisplayString0(inputString0 + digit);
		}
		displayMode = INPUT_MODE;
		clearOnNextDigit = false;
	}

	void addDecimalPoint(){
		displayMode = INPUT_MODE;

		if (clearOnNextDigit)
			setDisplayString("");

		String inputString = getDisplayString();
	
		// If the input string already contains a decimal point, don't
		//  do anything to it.
		if (inputString.indexOf(".") < 0)
			setDisplayString(new String(inputString + "."));
	}

	void processSignChange(){
		if (displayMode == INPUT_MODE)
		{
			String input = getDisplayString();

			if (input.length() > 0 && !input.equals("0"))
			{
				if (input.indexOf("-") == 0)
					setDisplayString(input.substring(1));

				else
					setDisplayString("-" + input);
			}
			
		}

		else if (displayMode == RESULT_MODE)
		{
			double numberInDisplay = getNumberInDisplay();
		
			if (numberInDisplay != 0)
				displayResult(-numberInDisplay);
		}
	}

	void clearAll()	{
		setDisplayString("0");
		setDisplayString0(" ");
		lastOperator = "0";
		lastNumber = 0;
		displayMode = INPUT_MODE;
		clearOnNextDigit = true;
	}

	void clearExisting(){
		setDisplayString("0");
		setDisplayString0(" ");
		clearOnNextDigit = true;
		displayMode = INPUT_MODE;
	}

	double getNumberInDisplay()	{
		String input = jlbOutput.getText();
		return Double.parseDouble(input);
	}

	void processOperator(String op) {
		if (displayMode != ERROR_MODE)
		{
			double numberInDisplay = getNumberInDisplay();

			if (!lastOperator.equals("0"))	
			{
				try
				{
					double result = processLastOperator();
					displayResult(result);
					lastNumber = result;
				}

				catch (DivideByZeroException e)
				{
				}
			}
		
			else
			{
				lastNumber = numberInDisplay;
			}
			
			clearOnNextDigit = true;
			lastOperator = op;
			String input = getDisplayString0()+lastOperator;
			setDisplayString0(input);		
		}
	}

	void processEquals(){
		double result = 0;

		if (displayMode != ERROR_MODE){
			try			
			{
				result = processLastOperator();
				displayResult(result);
			}
			
			catch (DivideByZeroException e)	{
				displayError("Cannot divide by zero!");
			}

			lastOperator = "0";
		}
	}

	double processLastOperator() throws DivideByZeroException {
		double result = 0;
		double numberInDisplay = getNumberInDisplay();
		result = numberInDisplay;                       // Added to display number on "="

		if (lastOperator.equals("/"))
		{
			if (numberInDisplay == 0)
				throw (new DivideByZeroException());
			result = lastNumber / numberInDisplay;
		}
		if (lastOperator.equals("Mod"))
		{
			if (numberInDisplay == 0)
				throw (new DivideByZeroException());
			result = lastNumber % numberInDisplay;
		}	
		if (lastOperator.equals("*"))
			result = lastNumber * numberInDisplay;

		if (lastOperator.equals("-"))
			result = lastNumber - numberInDisplay;

		if (lastOperator.equals("+"))
			result = lastNumber + numberInDisplay;
		
		if (lastOperator.equals("x^y")) {
			double x = (double) lastNumber;
			double y = (double) numberInDisplay;
		    result = (double) Math.pow(x, y);
		}
		if (lastOperator.equals("y rt x")) {
			double num = (double) lastNumber;
			double root = (double) getNumberInDisplay();
		    result = (double) Math.pow(num, 1.0 / root);
		}

		return result;
	}

	void displayResult(double result){
		setDisplayString(Double.toString(result));
		String inputString = getDisplayString();
		if (getDisplayString().indexOf("E")>= 0){
			setDisplayString(Double.toString(result));
		}
		else if ((getDisplayString().indexOf(".")>= 0) && (inputString.length() > 2 + fixDigits)) {
		   setDisplayString(getDisplayString().substring(0,2+fixDigits));
		}
		lastNumber = result;
		displayMode = RESULT_MODE;
		clearOnNextDigit = true;
	}

	void displayError(String errorMessage){
		setDisplayString(errorMessage);
		lastNumber = 0;
		displayMode = ERROR_MODE;
		clearOnNextDigit = true;
	}

	public static void main(String args[]) {
		Calculator calci = new Calculator();
		//Container contentPane = calci.getContentPane();
        //contentPane.setLayout(new BorderLayout());
		calci.setTitle("Java Swing Calculator");
		calci.setAlwaysOnTop( true );
        calci.setLocationByPlatform( true );
		calci.setSize(241, 217);
		calci.pack();
		calci.setLocation(400, 250);
		calci.setVisible(true);
		calci.setResizable(true);
	}
	
}		//End of Swing Calculator Class.

class DivideByZeroException extends Exception{
	private static final long serialVersionUID = 1L; 
	public DivideByZeroException()
	{
		super();
	}
	
	public DivideByZeroException(String s)
	{
		super(s);
	}
}

class CustomABOUTDialog extends JDialog implements ActionListener {
	private static final long serialVersionUID = 1L; 
	JButton jbnOk;

	CustomABOUTDialog(JFrame parent, String title, boolean modal){

		super(parent, title, modal);
		setBackground(Color.black);
		
		JPanel p1 = new JPanel(new FlowLayout(FlowLayout.CENTER));

		StringBuffer text = new StringBuffer();
		text.append("Calculator Information\n\n");
		text.append("Developers:	Hemanth, Randall\n");
		text.append("Version:	2.0");
		
		JTextArea jtAreaAbout = new JTextArea(5, 21);
		jtAreaAbout.setText(text.toString());
		jtAreaAbout.setFont(new Font("Times New Roman", 1, 13));
		jtAreaAbout.setEditable(false);

		p1.add(jtAreaAbout);
		p1.setBackground(Color.red);
		getContentPane().add(p1, BorderLayout.CENTER);

		JPanel p2 = new JPanel(new FlowLayout(FlowLayout.CENTER));
		jbnOk = new JButton(" OK ");
		jbnOk.addActionListener(this);

		p2.add(jbnOk);
		getContentPane().add(p2, BorderLayout.SOUTH);

		setLocation(408, 270);
		setResizable(true);

		addWindowListener(new WindowAdapter() {
				public void windowClosing(WindowEvent e)
				{
					Window aboutDialog = e.getWindow();
					aboutDialog.dispose();
				}
			}
		);

		pack();
	}

	public void actionPerformed(ActionEvent e)
	{
		if(e.getSource() == jbnOk)	{
			this.dispose();
		}
	}
	
}
