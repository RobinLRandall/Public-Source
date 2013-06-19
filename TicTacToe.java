
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.math.*;

/**
 * @author: Adam Taylor (D3M0L1$3®)
 *          Robin Randall  (Added AI logic for smarter game)
 * @version: 1.0.1.3.5
 * @release date: 06/19/2013
 * This is a simple Tic-tac-toe game written in Java
 * with some medeokre AI.
 * You go first,
 * can start a new game while in-game, or at the end of game 
 * and it asks
 * @Project Page:https://sourceforge.net/projects/tictactoe-javab/
 * @My Page: http://kickbanned.wordpress.com/
 * */

public class TicTacToe extends java.awt.Frame {
	static final  long serialVersionUID =0;
    private java.awt.MenuBar menuBar1;
    private java.awt.Menu menu1;
    private java.awt.MenuItem menuNewGame;
    private java.awt.MenuItem menuExit;
    private java.awt.MenuItem menuAbout;
    private static JButton button[];    
    private String sign = "X";
    private static String status[] = new String[ 10 ];  // Not sure why 10 (0-9)and not 9(0-8)
    private static String theWinner = "";               // Developer likes to count from 1?
    private boolean available = false;
    
    public TicTacToe() {
        super( "Tic Tac Toe" );
        initComponents();
    }
    
    private void initComponents() {
        setLayout( new java.awt.GridLayout( 3, 3, 1, 1 ) );
        setResizable( false );
        
        menuBar1    = new java.awt.MenuBar();
        menu1       = new java.awt.Menu();
        menuNewGame = new java.awt.MenuItem();
        menuExit    = new java.awt.MenuItem();
        menuAbout   = new java.awt.MenuItem();
        
        menu1.setLabel("File");
        menuNewGame.setLabel("New Game");
        menuNewGame.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                newGameActionPerformed(evt);
            }
        });
        
        menu1.add(menuNewGame);
        menuExit.setLabel("Exit");
        menuExit.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                exitActionPerformed(evt);
            }
        });
        
        menu1.add(menuExit);
        menuAbout.setLabel("About...");
        menuAbout.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                aboutActionPerformed(evt);
            }
        });
        
        menu1.add(menuAbout);
        menuBar1.add(menu1);
        
        addWindowListener(new java.awt.event.WindowAdapter() {
            public void windowClosing(java.awt.event.WindowEvent evt) {
                exitForm(evt);
            }
        });
        
        setMenuBar(menuBar1);
             
        button = new JButton[ 10 ];             // sets up the array of buttons - not 2D internally
        for ( int i = 1; i < 10; i++ ) {        //button[0] is not used
            button[ i ] = new JButton();
            button[ i ].setFocusPainted( false );
            button[ i ].setActionCommand( Integer.toString( i ) );
            button[ i ].setFont( new Font( "Dialog", 0, 48 ) );
            button[ i ].setPreferredSize( new Dimension( 100, 100 ) );
            button[ i ].setToolTipText( "Click to make your move" );
            button[ i ].addActionListener( new ActionListener() {
                public void actionPerformed( ActionEvent evt ) {
                    buttonAction( evt.getActionCommand() ); }
            } );
            add( button[ i ] );
        }     
        pack();
    }
    
    private void aboutActionPerformed(java.awt.event.ActionEvent evt) {
        JOptionPane.showMessageDialog( TicTacToe.this, "This simple game is created by \nD3M0L1SH3R.",
                                        "Tic Tac Toe", JOptionPane.INFORMATION_MESSAGE );
    }

    private void exitActionPerformed(java.awt.event.ActionEvent evt) {
        System.exit( 0 );
    }

    private void newGameActionPerformed(java.awt.event.ActionEvent evt) {
        setNewGame();
    }

    private void exitForm(java.awt.event.WindowEvent evt) {
        System.exit( 0 );
    }
    
    public static void main( String args[] ) {
         new TicTacToe().setVisible(true);              //Changed depecated ".show()" to "setVisible()"
         setNewGame();
    }
    
    private void buttonAction( String btn ) {
        int index = Integer.parseInt( btn );
        if ( button[ index ].getText() == "" ) {
            button[ index ].setText( sign );       // "sign" is actually the "X" choice
            status[ index ] = sign;
            checkGameStatus();                     // Check for a winner.
            nextMove();
        }
        else
            JOptionPane.showMessageDialog( TicTacToe.this,
                        "This square is already occupied, \nplease try another one.",
                                            "Oops...", JOptionPane.ERROR_MESSAGE );
    }
    private boolean testWinDiag(String sign, int s0,int s1,int s2,int s3,int s4,int s5,int s6) {
    	if (   (button[ s0 ].getText() == "" )
       		 && 
       	   (     ((button[s1].getText() == sign) 
       		 &&  (button[s2].getText() == sign))
       	 ||      ((button[s3].getText() == sign) 
       	     &&  (button[s4].getText() == sign))
       	 ||      ((button[s5].getText() == sign) 
       		 &&  (button[s6].getText() == sign)) )  ) {    		                                  
       		button[ s0 ].setText( "O" );
       		//status[ s0 ] = sign; 
       		return (true);
    	}	
    	else {return (false);
       	}    
    }
    private boolean testWinSide(String sign, int s0,int s1,int s2,int s3,int s4) {
    	if (   (button[ s0 ].getText() == "" )
       		 && 
       	   (     ((button[s1].getText() == sign) 
       		 &&  (button[s2].getText() == sign))
       	 ||      ((button[s3].getText() == sign) 
       		 &&  (button[s4].getText() == sign)) )  ) {    		                                  
       		button[ s0 ].setText( "O" );
       		//status[ s0 ] = sign; 
       		return (true);
    	}	
    	else {return (false);
       	}
    }	
   	private void nextMove() {
   		// Check for a win by "O"
   		if (testWinDiag("O",1,2,3,5,9,4,7)) {
   			status[ 1 ]="O";
   		}
    	else if (testWinSide("O",2,1,3,5,8)) {
       		status[ 2 ] = "O"; 
       	}    	
    	else if (testWinDiag("O",3,1,2,5,7,6,9)) {
       		status[ 3 ] = "O"; 
       	}    	
    	else if (testWinSide("O",4,1,7,5,6)) {
       		status[ 4 ] = "O"; 
       	}    	
    	else if (   (button[ 5 ].getText() == "" )
          		 && 
          	   (     ((button[1].getText() == "O") 
          		 &&  (button[9].getText() == "O"))
          	 ||      ((button[2].getText() == "O") 
          	     &&  (button[8].getText() == "O"))
          	 ||      ((button[3].getText() == "O") 
          		 &&  (button[7].getText() == "O")) 
             ||      ((button[4].getText() == "O") 
                 &&  (button[6].getText() == "O")) ) ) {    		                                  
          		button[ 5 ].setText( "O" );
          		status[ 5 ] = "O"; 
       	} 
    	else if (testWinSide("O",6,3,9,4,5)){
       		status[ 6 ] = "O"; 
       	}    	
    	else if (testWinDiag("O",7,1,4,3,5,8,9)){
       		status[ 7 ] = "O"; 
    	}
    	else if (testWinSide("O",8,2,5,7,9)){
       		status[ 8 ] = "O";  
           }    	
    	else if (testWinDiag("O",9,1,5,3,6,7,8)){
       		status[ 9 ] = "O"; 
    	} 
   		// Check to block win by "X"
    	else if (testWinDiag("X",1,2,3,5,9,4,7)){
   			status[ 1 ]="O";
   		}
    	else if (testWinSide("X",2,1,3,5,8)){
       		status[ 2 ] = "O"; 
       	}    	
    	else if (testWinDiag("X",3,1,2,5,7,6,9)){
       		status[ 3 ] = "O"; 
       	}    	
    	else if (testWinSide("X",4,1,7,5,6)){
       		status[ 4 ] = "O"; 
       	}    	
    	else if (   (button[ 5 ].getText() == "" )
          		 && 
          	   (     ((button[1].getText() == "X") 
          		 &&  (button[9].getText() == "X"))
          	 ||      ((button[2].getText() == "X") 
          	     &&  (button[8].getText() == "X"))
          	 ||      ((button[3].getText() == "X") 
          		 &&  (button[7].getText() == "X")) 
             ||      ((button[4].getText() == "X") 
                 &&  (button[6].getText() == "X")) ) ) {    		                                  
          		button[ 5 ].setText( "O" );
          		status[ 5 ] = "O"; 
       	} 
    	else if (testWinSide("X",6,3,9,4,5)) {
       		status[ 6 ] = "O"; 
       	}    	
    	else if (testWinDiag("X",7,1,4,3,5,8,9)) {
       		status[ 7 ] = "O"; 
    	}
    	else if (testWinSide("X",8,2,5,7,9)) {
       		status[ 8 ] = "O";  
           }    	
    	else if (testWinDiag("X",9,1,5,3,6,7,8)) {
       		status[ 9 ] = "O"; 
    	} 
    	//else if ( button[ 5 ].getText() == "" ){   // "O" picks center square if it is open
         //    button[ 5 ].setText( "O" );           // Otherwise it picks a random open square
         //    status[ 5 ] = "O";                    // If difficulty levels are added, I recommend
        //}                                          // this be the "Easy" level
        else {
            int move = randomMove();              //randomMove() is guaranteed to eventually (I think)
            if ( button[ move ].getText() != "" ) //pick an open square if there is one, however it
                nextMove();                       //could be optimized to pick only open squares
            else {
                button[ move ].setText( "O" );
                status[ move ] = "O";
            }
        }
        checkGameStatus();
    }
    
    private int randomMove() { // Makes a random move for "O" (The computer)
        int attempt = 0;       // This can be improved to make "smart" moves
                               // but for small kids, random moves this let them win       
        attempt = ( 1 + ( int ) ( Math.random() * 9 ) );        
        return attempt;
    }
    
    public static void setNewGame() {          //Sets up anew game with all "blank" squares
        for ( int j = 1; j < 10; j++ ) {
            button[ j ].setText( "" );
            status[ j ] = "";            
        }
        theWinner = "";
    }
    private void checkGame(int s1, int s2, int s3, int s4, int s5, int s6) { // Used in checkGameStatus
        if ( ( status[ s1 ] != "" ) && ( status[ s2 ] == status [ s3 ] 
                && status[ s4 ] == status[ s5 ] ) ){
                theWinner = status[ s6 ];
                gameStop( theWinner );
        }
    }
    private void checkGameStatus() {  //This section performed the identical algorithm 8 times 
    	checkGame(1,1,2,2,3,1);       //except for the integer arguments. This trimmed the program
    	checkGame(4,4,5,5,6,4);       // considerably
    	checkGame(7,7,8,8,9,7);
    	checkGame(1,1,4,4,7,1);
    	checkGame(2,2,5,5,8,2);
    	checkGame(3,3,6,6,9,3);
    	checkGame(1,1,5,5,9,1);
    	checkGame(3,3,5,5,7,3);
                
        found: {
          for ( int a = 1; a < 10; a++ ) {  // Looks for an empty square
            if ( status[ a ] == "" ){
                available = true;
                break found;
            }
            else
                available = false;
          }
        }
        
        if ( !available )                   //If all squares are occupied then it is a tie!
            gameStop( "tie" );  
    }
    
    private void gameStop( String win ) {  //Stops the game when tied or someone has won
        if ( win == "tie" ){
            JOptionPane.showMessageDialog( null, "It's a tie, baby!!! \nLets play again!",
                                        "That was a game...", JOptionPane.INFORMATION_MESSAGE );
            setNewGame();
        }
        else {
            String output = "The player \"" + win + "\" has won!!! \nWould you like to play again?";
            int choice = JOptionPane.showConfirmDialog( null, output,
                "Congratulations!", JOptionPane.YES_NO_OPTION, JOptionPane.INFORMATION_MESSAGE );
            if ( choice == 0 )
                setNewGame();        //Yes
            else
                System.exit( 0 );    //No
        }
    }
}

