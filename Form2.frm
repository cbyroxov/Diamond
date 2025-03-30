VERSION 5.00
Begin VB.Form main_window 
   BorderStyle     =   1  'Fixed Single
   Caption         =   "PlayStation OS ROM Modifier"
   ClientHeight    =   6480
   ClientLeft      =   150
   ClientTop       =   435
   ClientWidth     =   7680
   LinkTopic       =   "Form2"
   MaxButton       =   0   'False
   MinButton       =   0   'False
   ScaleHeight     =   6480
   ScaleWidth      =   7680
   StartUpPosition =   2  'CenterScreen
   Begin VB.Frame Frame8 
      Caption         =   "Pitch"
      Height          =   1335
      Left            =   5760
      TabIndex        =   41
      Top             =   4560
      Width           =   1695
      Begin VB.Line Line2 
         X1              =   0
         X2              =   1680
         Y1              =   120
         Y2              =   1320
      End
      Begin VB.Line Line1 
         X1              =   0
         X2              =   1680
         Y1              =   1320
         Y2              =   120
      End
   End
   Begin VB.Frame Frame7 
      Caption         =   "Reverberation"
      Height          =   1335
      Left            =   3000
      TabIndex        =   40
      Top             =   4560
      Width           =   2655
      Begin VB.OptionButton Option6 
         Caption         =   "No Reverb"
         Height          =   255
         Left            =   120
         TabIndex        =   47
         Top             =   240
         Width           =   1095
      End
      Begin VB.OptionButton Option5 
         Caption         =   "Room"
         Height          =   255
         Left            =   1560
         TabIndex        =   46
         Top             =   720
         Width           =   735
      End
      Begin VB.OptionButton Option4 
         Caption         =   "Studio Small"
         Height          =   255
         Left            =   120
         TabIndex        =   45
         Top             =   960
         Width           =   1455
      End
      Begin VB.OptionButton Option3 
         Caption         =   "Studio Medium"
         Height          =   255
         Left            =   120
         TabIndex        =   44
         Top             =   720
         Width           =   1455
      End
      Begin VB.OptionButton Option2 
         Caption         =   "Studio Large"
         Height          =   255
         Left            =   120
         TabIndex        =   43
         Top             =   480
         Width           =   1215
      End
      Begin VB.OptionButton Option1 
         Caption         =   "Hall"
         Height          =   255
         Left            =   1320
         TabIndex        =   42
         Top             =   240
         Width           =   615
      End
   End
   Begin VB.Frame Frame6 
      Caption         =   "Sound Effects [.VAG]"
      Height          =   1335
      Left            =   120
      TabIndex        =   33
      Top             =   4560
      Width           =   2775
      Begin VB.CommandButton Command9 
         Caption         =   "Import"
         Height          =   255
         Left            =   2040
         TabIndex        =   39
         Top             =   960
         Width           =   615
      End
      Begin VB.CommandButton Command8 
         Caption         =   "Import"
         Height          =   255
         Left            =   840
         TabIndex        =   38
         Top             =   600
         Width           =   615
      End
      Begin VB.CommandButton Command7 
         Caption         =   "Import"
         Height          =   255
         Left            =   1440
         TabIndex        =   37
         Top             =   240
         Width           =   615
      End
      Begin VB.Label Label11 
         Caption         =   "Reversed Breaking Glass :"
         Height          =   255
         Left            =   120
         TabIndex        =   36
         Top             =   960
         Width           =   1935
      End
      Begin VB.Label Label10 
         Caption         =   "Chimes :"
         Height          =   375
         Left            =   120
         TabIndex        =   35
         Top             =   600
         Width           =   1935
      End
      Begin VB.Label Label1 
         Caption         =   "Sawtooth Synth :"
         Height          =   375
         Left            =   120
         TabIndex        =   34
         Top             =   240
         Width           =   1935
      End
   End
   Begin VB.Frame Frame5 
      Caption         =   "Main Menu Rainbow Gradient"
      Height          =   1815
      Left            =   4680
      TabIndex        =   29
      Top             =   960
      Width           =   2775
      Begin VB.TextBox Text8 
         Appearance      =   0  'Flat
         BackColor       =   &H00FF8080&
         Height          =   285
         Index           =   1
         Left            =   480
         TabIndex        =   32
         Top             =   1200
         Width           =   2175
      End
      Begin VB.TextBox Text8 
         Appearance      =   0  'Flat
         BackColor       =   &H0080FF80&
         Height          =   285
         Index           =   0
         Left            =   480
         TabIndex        =   31
         Top             =   840
         Width           =   2175
      End
      Begin VB.TextBox Text7 
         Appearance      =   0  'Flat
         BackColor       =   &H008080FF&
         Height          =   285
         Left            =   480
         TabIndex        =   30
         Top             =   480
         Width           =   2175
      End
      Begin VB.Shape Shape10 
         FillColor       =   &H00FF0000&
         FillStyle       =   0  'Solid
         Height          =   255
         Left            =   120
         Top             =   1200
         Width           =   255
      End
      Begin VB.Shape Shape9 
         FillColor       =   &H0000FF00&
         FillStyle       =   0  'Solid
         Height          =   255
         Left            =   120
         Top             =   840
         Width           =   255
      End
      Begin VB.Shape Shape8 
         FillColor       =   &H000000FF&
         FillStyle       =   0  'Solid
         Height          =   255
         Left            =   120
         Top             =   480
         Width           =   255
      End
   End
   Begin VB.CommandButton Command6 
      Caption         =   "Exit"
      Height          =   375
      Left            =   5760
      TabIndex        =   28
      Top             =   6000
      Width           =   1695
   End
   Begin VB.CommandButton Command5 
      Caption         =   "Apply Changes"
      Height          =   375
      Left            =   120
      TabIndex        =   27
      Top             =   6000
      Width           =   1935
   End
   Begin VB.CommandButton Command4 
      Caption         =   "Import"
      Height          =   255
      Index           =   4
      Left            =   5760
      TabIndex        =   26
      Top             =   3960
      Width           =   615
   End
   Begin VB.CommandButton Command4 
      Caption         =   "Import"
      Height          =   255
      Index           =   3
      Left            =   5520
      TabIndex        =   25
      Top             =   3240
      Width           =   615
   End
   Begin VB.CommandButton Command4 
      Caption         =   "Import"
      Height          =   255
      Index           =   2
      Left            =   3840
      TabIndex        =   22
      Top             =   3600
      Width           =   615
   End
   Begin VB.CommandButton Command4 
      Caption         =   "Import"
      Height          =   255
      Index           =   1
      Left            =   3720
      TabIndex        =   20
      Top             =   3960
      Width           =   615
   End
   Begin VB.PictureBox Picture1 
      Height          =   735
      Left            =   360
      Picture         =   "Form2.frx":0000
      ScaleHeight     =   675
      ScaleWidth      =   6915
      TabIndex        =   0
      Top             =   120
      Width           =   6975
      Begin VB.Line Line3 
         X1              =   6960
         X2              =   6960
         Y1              =   0
         Y2              =   720
      End
   End
   Begin VB.Frame Frame1 
      Caption         =   "PlayStation Sphere Color"
      Height          =   1815
      Left            =   120
      TabIndex        =   1
      Top             =   960
      Width           =   4455
      Begin VB.Frame Frame2 
         Caption         =   "Inner"
         Height          =   1335
         Left            =   240
         TabIndex        =   2
         Top             =   240
         Width           =   1935
         Begin VB.TextBox Text3 
            Appearance      =   0  'Flat
            BackColor       =   &H00FF8080&
            Height          =   285
            Left            =   480
            TabIndex        =   6
            ToolTipText     =   "Set RGB Color for BLUE"
            Top             =   960
            Width           =   1335
         End
         Begin VB.TextBox Text2 
            Appearance      =   0  'Flat
            BackColor       =   &H0080FF80&
            Height          =   285
            Left            =   480
            TabIndex        =   5
            ToolTipText     =   "Set RGB Color for GREEN"
            Top             =   600
            Width           =   1335
         End
         Begin VB.TextBox Text1 
            Appearance      =   0  'Flat
            BackColor       =   &H008080FF&
            Height          =   285
            Left            =   480
            TabIndex        =   4
            ToolTipText     =   "Set RGB Color for RED"
            Top             =   240
            Width           =   1335
         End
         Begin VB.Shape Shape4 
            FillColor       =   &H00FF0000&
            FillStyle       =   0  'Solid
            Height          =   255
            Left            =   120
            Top             =   960
            Width           =   255
         End
         Begin VB.Shape Shape3 
            FillColor       =   &H0000FF00&
            FillStyle       =   0  'Solid
            Height          =   255
            Left            =   120
            Top             =   600
            Width           =   255
         End
         Begin VB.Shape Shape1 
            FillColor       =   &H000000FF&
            FillStyle       =   0  'Solid
            Height          =   255
            Left            =   120
            Top             =   240
            Width           =   255
         End
      End
      Begin VB.Frame Frame3 
         Caption         =   "Outer"
         Height          =   1335
         Left            =   2280
         TabIndex        =   3
         Top             =   240
         Width           =   1935
         Begin VB.TextBox Text6 
            Appearance      =   0  'Flat
            BackColor       =   &H00FF8080&
            Height          =   285
            Left            =   480
            TabIndex        =   9
            ToolTipText     =   "Set RGB Color for BLUE"
            Top             =   960
            Width           =   1335
         End
         Begin VB.TextBox Text5 
            Appearance      =   0  'Flat
            BackColor       =   &H0080FF80&
            Height          =   285
            Left            =   480
            TabIndex        =   8
            ToolTipText     =   "Set RGB Color for GREEN"
            Top             =   600
            Width           =   1335
         End
         Begin VB.TextBox Text4 
            Appearance      =   0  'Flat
            BackColor       =   &H008080FF&
            Height          =   285
            Left            =   480
            TabIndex        =   7
            ToolTipText     =   "Set RGB Color for RED"
            Top             =   240
            Width           =   1335
         End
         Begin VB.Shape Shape7 
            FillColor       =   &H00FF0000&
            FillStyle       =   0  'Solid
            Height          =   255
            Left            =   120
            Top             =   960
            Width           =   255
         End
         Begin VB.Shape Shape6 
            FillColor       =   &H0000FF00&
            FillStyle       =   0  'Solid
            Height          =   255
            Left            =   120
            Top             =   600
            Width           =   255
         End
         Begin VB.Shape Shape5 
            FillColor       =   &H000000FF&
            FillStyle       =   0  'Solid
            Height          =   255
            Left            =   120
            Top             =   240
            Width           =   255
         End
      End
   End
   Begin VB.Frame Frame4 
      Caption         =   "TIM Modification [.TIM]"
      Height          =   1575
      Left            =   120
      TabIndex        =   10
      Top             =   2880
      Width           =   7455
      Begin VB.CommandButton Command4 
         Caption         =   "Import"
         Height          =   255
         Index           =   0
         Left            =   3480
         TabIndex        =   18
         Top             =   360
         Width           =   615
      End
      Begin VB.CommandButton Command3 
         Caption         =   "Import"
         Height          =   255
         Left            =   1080
         TabIndex        =   14
         Top             =   1080
         Width           =   615
      End
      Begin VB.CommandButton Command2 
         Caption         =   "Import"
         Height          =   255
         Left            =   2040
         TabIndex        =   13
         Top             =   720
         Width           =   615
      End
      Begin VB.CommandButton Command1 
         Caption         =   "Import"
         Height          =   255
         Index           =   0
         Left            =   1080
         TabIndex        =   12
         Top             =   360
         Width           =   615
      End
      Begin VB.Label Label9 
         Caption         =   "Memory Card :"
         Height          =   255
         Left            =   4560
         TabIndex        =   24
         Top             =   1080
         Width           =   1095
      End
      Begin VB.Label Label8 
         Caption         =   "CD Player :"
         Height          =   255
         Index           =   0
         Left            =   4560
         TabIndex        =   23
         Top             =   360
         Width           =   1215
      End
      Begin VB.Label Label7 
         Caption         =   "Main Menu :"
         Height          =   255
         Left            =   2760
         TabIndex        =   21
         Top             =   720
         Width           =   1455
      End
      Begin VB.Label Label6 
         Caption         =   "Crosshair :"
         Height          =   255
         Left            =   2760
         TabIndex        =   19
         Top             =   1080
         Width           =   1215
      End
      Begin VB.Label Label5 
         Caption         =   "Cursor :"
         Height          =   255
         Left            =   2760
         TabIndex        =   17
         Top             =   360
         Width           =   1455
      End
      Begin VB.Label Label4 
         Caption         =   "PlayStation :"
         Height          =   255
         Left            =   120
         TabIndex        =   16
         Top             =   1080
         Width           =   2535
      End
      Begin VB.Label Label3 
         Caption         =   "Computer Entertainment :"
         Height          =   255
         Left            =   120
         TabIndex        =   15
         Top             =   720
         Width           =   2535
      End
      Begin VB.Label Label2 
         Caption         =   "Sony Logo :    "
         Height          =   255
         Index           =   0
         Left            =   120
         TabIndex        =   11
         Top             =   360
         Width           =   1575
      End
   End
   Begin VB.Label Label12 
      Caption         =   "DevTip : Frames that has a cross means that the features will be coming soon."
      Height          =   495
      Left            =   2160
      TabIndex        =   48
      Top             =   6000
      Width           =   3375
   End
   Begin VB.Shape Shape2 
      Height          =   255
      Left            =   360
      Top             =   1920
      Width           =   255
   End
End
Attribute VB_Name = "main_window"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False

Private Sub Command6_Click()
End
End Sub

Private Sub Label13_Click()

End Sub

Private Sub Label14_Click()

End Sub
