namespace Demo
{
    partial class Form1
    {
        /// <summary>
        /// 必需的设计器变量。
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// 清理所有正在使用的资源。
        /// </summary>
        /// <param name="disposing">如果应释放托管资源，为 true；否则为 false。</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows 窗体设计器生成的代码

        /// <summary>
        /// 设计器支持所需的方法 - 不要
        /// 使用代码编辑器修改此方法的内容。
        /// </summary>
        private void InitializeComponent()
        {
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(Form1));
            this.bnInit = new System.Windows.Forms.Button();
            this.bnOpen = new System.Windows.Forms.Button();
            this.bnEnroll = new System.Windows.Forms.Button();
            this.bnVerify = new System.Windows.Forms.Button();
            this.bnFree = new System.Windows.Forms.Button();
            this.bnClose = new System.Windows.Forms.Button();
            this.bnIdentify = new System.Windows.Forms.Button();
            this.picFPImg = new System.Windows.Forms.PictureBox();
            this.label1 = new System.Windows.Forms.Label();
            this.cmbIdx = new System.Windows.Forms.ComboBox();
            this.btnOutput = new System.Windows.Forms.Button();
            this.txtTemplate1 = new System.Windows.Forms.TextBox();
            this.txtTemplate2 = new System.Windows.Forms.TextBox();
            this.btMatch = new System.Windows.Forms.Button();
            this.tabControl1 = new System.Windows.Forms.TabControl();
            this.tabPage1 = new System.Windows.Forms.TabPage();
            this.btnImport = new System.Windows.Forms.Button();
            this.textRes = new System.Windows.Forms.RichTextBox();
            ((System.ComponentModel.ISupportInitialize)(this.picFPImg)).BeginInit();
            this.tabControl1.SuspendLayout();
            this.tabPage1.SuspendLayout();
            this.SuspendLayout();
            // 
            // bnInit
            // 
            this.bnInit.Location = new System.Drawing.Point(14, 7);
            this.bnInit.Name = "bnInit";
            this.bnInit.Size = new System.Drawing.Size(75, 23);
            this.bnInit.TabIndex = 0;
            this.bnInit.Text = "Initialize";
            this.bnInit.UseVisualStyleBackColor = true;
            this.bnInit.Click += new System.EventHandler(this.bnInit_Click);
            // 
            // bnOpen
            // 
            this.bnOpen.Enabled = false;
            this.bnOpen.Location = new System.Drawing.Point(14, 51);
            this.bnOpen.Name = "bnOpen";
            this.bnOpen.Size = new System.Drawing.Size(75, 23);
            this.bnOpen.TabIndex = 1;
            this.bnOpen.Text = "Open";
            this.bnOpen.UseVisualStyleBackColor = true;
            this.bnOpen.Click += new System.EventHandler(this.bnOpen_Click);
            // 
            // bnEnroll
            // 
            this.bnEnroll.Enabled = false;
            this.bnEnroll.Location = new System.Drawing.Point(59, 100);
            this.bnEnroll.Name = "bnEnroll";
            this.bnEnroll.Size = new System.Drawing.Size(193, 23);
            this.bnEnroll.TabIndex = 2;
            this.bnEnroll.Text = "Enroll(Add To DataBase)";
            this.bnEnroll.UseVisualStyleBackColor = true;
            this.bnEnroll.Click += new System.EventHandler(this.bnEnroll_Click);
            // 
            // bnVerify
            // 
            this.bnVerify.Enabled = false;
            this.bnVerify.Location = new System.Drawing.Point(59, 172);
            this.bnVerify.Name = "bnVerify";
            this.bnVerify.Size = new System.Drawing.Size(193, 23);
            this.bnVerify.TabIndex = 3;
            this.bnVerify.Text = "Match Mode(1:1)";
            this.bnVerify.UseVisualStyleBackColor = true;
            this.bnVerify.Click += new System.EventHandler(this.bnVerify_Click);
            // 
            // bnFree
            // 
            this.bnFree.Enabled = false;
            this.bnFree.Location = new System.Drawing.Point(216, 51);
            this.bnFree.Name = "bnFree";
            this.bnFree.Size = new System.Drawing.Size(75, 23);
            this.bnFree.TabIndex = 4;
            this.bnFree.Text = "Finalize";
            this.bnFree.UseVisualStyleBackColor = true;
            this.bnFree.Click += new System.EventHandler(this.bnFree_Click);
            // 
            // bnClose
            // 
            this.bnClose.Enabled = false;
            this.bnClose.Location = new System.Drawing.Point(216, 12);
            this.bnClose.Name = "bnClose";
            this.bnClose.Size = new System.Drawing.Size(75, 23);
            this.bnClose.TabIndex = 5;
            this.bnClose.Text = "Close";
            this.bnClose.UseVisualStyleBackColor = true;
            this.bnClose.Click += new System.EventHandler(this.bnClose_Click);
            // 
            // bnIdentify
            // 
            this.bnIdentify.Enabled = false;
            this.bnIdentify.Location = new System.Drawing.Point(59, 143);
            this.bnIdentify.Name = "bnIdentify";
            this.bnIdentify.Size = new System.Drawing.Size(193, 23);
            this.bnIdentify.TabIndex = 6;
            this.bnIdentify.Text = "Identiy Mode(1:N)";
            this.bnIdentify.UseVisualStyleBackColor = true;
            this.bnIdentify.Click += new System.EventHandler(this.bnIdentify_Click);
            // 
            // picFPImg
            // 
            this.picFPImg.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(224)))), ((int)(((byte)(224)))), ((int)(((byte)(224)))));
            this.picFPImg.BackgroundImageLayout = System.Windows.Forms.ImageLayout.Center;
            this.picFPImg.Location = new System.Drawing.Point(6, 6);
            this.picFPImg.Name = "picFPImg";
            this.picFPImg.Size = new System.Drawing.Size(267, 269);
            this.picFPImg.SizeMode = System.Windows.Forms.PictureBoxSizeMode.Zoom;
            this.picFPImg.TabIndex = 8;
            this.picFPImg.TabStop = false;
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(95, 51);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(41, 12);
            this.label1.TabIndex = 9;
            this.label1.Text = "Index:";
            // 
            // cmbIdx
            // 
            this.cmbIdx.FormattingEnabled = true;
            this.cmbIdx.Location = new System.Drawing.Point(142, 51);
            this.cmbIdx.Name = "cmbIdx";
            this.cmbIdx.Size = new System.Drawing.Size(40, 20);
            this.cmbIdx.TabIndex = 10;
            // 
            // btnOutput
            // 
            this.btnOutput.Enabled = false;
            this.btnOutput.Location = new System.Drawing.Point(145, 281);
            this.btnOutput.Name = "btnOutput";
            this.btnOutput.Size = new System.Drawing.Size(131, 23);
            this.btnOutput.TabIndex = 12;
            this.btnOutput.Text = "Output BMP";
            this.btnOutput.UseVisualStyleBackColor = true;
            this.btnOutput.Click += new System.EventHandler(this.btCaptureBmp_Click);
            // 
            // txtTemplate1
            // 
            this.txtTemplate1.Location = new System.Drawing.Point(14, 233);
            this.txtTemplate1.Name = "txtTemplate1";
            this.txtTemplate1.Size = new System.Drawing.Size(268, 21);
            this.txtTemplate1.TabIndex = 13;
            this.txtTemplate1.Text = resources.GetString("txtTemplate1.Text");
            // 
            // txtTemplate2
            // 
            this.txtTemplate2.Location = new System.Drawing.Point(14, 271);
            this.txtTemplate2.Name = "txtTemplate2";
            this.txtTemplate2.Size = new System.Drawing.Size(268, 21);
            this.txtTemplate2.TabIndex = 14;
            this.txtTemplate2.Text = resources.GetString("txtTemplate2.Text");
            // 
            // btMatch
            // 
            this.btMatch.Enabled = false;
            this.btMatch.Location = new System.Drawing.Point(59, 307);
            this.btMatch.Name = "btMatch";
            this.btMatch.Size = new System.Drawing.Size(178, 23);
            this.btMatch.TabIndex = 15;
            this.btMatch.Text = "Match Finger Template Data";
            this.btMatch.UseVisualStyleBackColor = true;
            this.btMatch.Click += new System.EventHandler(this.btMatch_Click);
            // 
            // tabControl1
            // 
            this.tabControl1.Controls.Add(this.tabPage1);
            this.tabControl1.Location = new System.Drawing.Point(321, 12);
            this.tabControl1.Name = "tabControl1";
            this.tabControl1.SelectedIndex = 0;
            this.tabControl1.Size = new System.Drawing.Size(287, 336);
            this.tabControl1.TabIndex = 16;
            this.tabControl1.Tag = "S";
            // 
            // tabPage1
            // 
            this.tabPage1.Controls.Add(this.btnImport);
            this.tabPage1.Controls.Add(this.picFPImg);
            this.tabPage1.Controls.Add(this.btnOutput);
            this.tabPage1.Location = new System.Drawing.Point(4, 22);
            this.tabPage1.Name = "tabPage1";
            this.tabPage1.Padding = new System.Windows.Forms.Padding(3);
            this.tabPage1.Size = new System.Drawing.Size(279, 310);
            this.tabPage1.TabIndex = 0;
            this.tabPage1.Text = "Image Convert(Charge)";
            this.tabPage1.UseVisualStyleBackColor = true;
            // 
            // btnImport
            // 
            this.btnImport.Enabled = false;
            this.btnImport.Location = new System.Drawing.Point(8, 281);
            this.btnImport.Name = "btnImport";
            this.btnImport.Size = new System.Drawing.Size(131, 23);
            this.btnImport.TabIndex = 13;
            this.btnImport.Text = "Import BMP";
            this.btnImport.UseVisualStyleBackColor = true;
            this.btnImport.Click += new System.EventHandler(this.btnImport_Click);
            // 
            // textRes
            // 
            this.textRes.Location = new System.Drawing.Point(6, 354);
            this.textRes.Name = "textRes";
            this.textRes.Size = new System.Drawing.Size(595, 207);
            this.textRes.TabIndex = 17;
            this.textRes.Text = "";
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 12F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(611, 565);
            this.Controls.Add(this.textRes);
            this.Controls.Add(this.tabControl1);
            this.Controls.Add(this.btMatch);
            this.Controls.Add(this.txtTemplate2);
            this.Controls.Add(this.txtTemplate1);
            this.Controls.Add(this.cmbIdx);
            this.Controls.Add(this.label1);
            this.Controls.Add(this.bnIdentify);
            this.Controls.Add(this.bnClose);
            this.Controls.Add(this.bnFree);
            this.Controls.Add(this.bnVerify);
            this.Controls.Add(this.bnEnroll);
            this.Controls.Add(this.bnOpen);
            this.Controls.Add(this.bnInit);
            this.MaximizeBox = false;
            this.MinimizeBox = false;
            this.Name = "Form1";
            this.Text = "C# ZKFinger Demo v0.2";
            this.Load += new System.EventHandler(this.Form1_Load);
            ((System.ComponentModel.ISupportInitialize)(this.picFPImg)).EndInit();
            this.tabControl1.ResumeLayout(false);
            this.tabPage1.ResumeLayout(false);
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Button bnInit;
        private System.Windows.Forms.Button bnOpen;
        private System.Windows.Forms.Button bnEnroll;
        private System.Windows.Forms.Button bnVerify;
        private System.Windows.Forms.Button bnFree;
        private System.Windows.Forms.Button bnClose;
        private System.Windows.Forms.Button bnIdentify;
        private System.Windows.Forms.PictureBox picFPImg;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.ComboBox cmbIdx;
        private System.Windows.Forms.Button btnOutput;
        private System.Windows.Forms.TextBox txtTemplate1;
        private System.Windows.Forms.TextBox txtTemplate2;
        private System.Windows.Forms.Button btMatch;
        private System.Windows.Forms.TabControl tabControl1;
        private System.Windows.Forms.TabPage tabPage1;
        private System.Windows.Forms.Button btnImport;
        private System.Windows.Forms.RichTextBox textRes;
    }
}

