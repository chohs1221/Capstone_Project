/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.c
  * @brief          : Main program body
  ******************************************************************************
  * @attention
  *
  * <h2><center>&copy; Copyright (c) 2021 STMicroelectronics.
  * All rights reserved.</center></h2>
  *
  * This software component is licensed by ST under BSD 3-Clause license,
  * the "License"; You may not use this file except in compliance with the
  * License. You may obtain a copy of the License at:
  *                        opensource.org/licenses/BSD-3-Clause
  *
  ******************************************************************************
  */
/* USER CODE END Header */
/* Includes ------------------------------------------------------------------*/
#include "main.h"
#include "adc.h"
#include "dma.h"
#include "tim.h"
#include "usart.h"
#include "gpio.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */

/* USER CODE END Includes */

/* Private typedef -----------------------------------------------------------*/
/* USER CODE BEGIN PTD */

/* USER CODE END PTD */

/* Private define ------------------------------------------------------------*/
/* USER CODE BEGIN PD */
/* USER CODE END PD */

/* Private macro -------------------------------------------------------------*/
/* USER CODE BEGIN PM */

/* USER CODE END PM */

/* Private variables ---------------------------------------------------------*/

/* USER CODE BEGIN PV */
unsigned int cnt_main = 0;
unsigned int cnt_adc1 = 0;
int cnt;
int adc;
int y;
uint32_t adc1_buffer[10];		//current,psd
/* USER CODE END PV */

/* Private function prototypes -----------------------------------------------*/
void SystemClock_Config(void);
/* USER CODE BEGIN PFP */

/* USER CODE END PFP */

/* Private user code ---------------------------------------------------------*/
/* USER CODE BEGIN 0 */
int dir =0;
int i=0;
int o = 0;
int duty=0;
int k =0;
int g = 0;
int count_sec = 0;
int cnnt = 0;

int m = 0;
int n = 0;

int h = 0;

int a=0;
int b=0;
int c=0;
int d=0;

int process1 = 0;
int process2 = 0;
int process3 = 0;
//-----------------------------Controller-------------------------------//
							//moving average filter//
#define MAF_SIZE 50
double g_rawData[MAF_SIZE] = {0,};
double g_SUM_Data = 0.0;
double g_MAF_Data = 0.0;
int g_MAF_CNT  = 0;

#define MAF_SIZE2 100
double g_rawData2[MAF_SIZE2] = {0,};
double g_SUM_Data2 = 0.0;
double g_MAF_Data2 = 0.0;
int g_MAF_CNT2  = 0;

#define MAF_SIZE3 100
double g_rawData3[MAF_SIZE3] = {0,};
double g_SUM_Data3 = 0.0;
double g_MAF_Data3 = 0.0;
int g_MAF_CNT3  = 0;

							//PWM//
int speed;

int f_l_speed;	//front left
int f_r_speed;	//front right
int u_speed;	//upper

int p_speed;	//pump
int b_l_speed;	//back left
int b_r_speed;	//back right
int u_speed2;	//upper2

							//Angle//
							//Upper Side//		//not yet
int32_t enc3 = 0;
int pre_enc3 = 0;
int enc_diff3 = 0;
int linear_enc3 = 0;
int pre_linear_enc3 = 0;
int dif_linear_enc3 = 0;
volatile float Target_Angle3 = 0.0;			//2rad >> 11.31cm << r = 0.018
volatile float Ang_Error3 = 0.0;
volatile float pre_Ang_Error3 = 0.0;
volatile float Angle3 = 0.0;
volatile float pre_Angle3 = 0.0;
volatile float Angle_Control3 = 0.0;
volatile float Ang_Kp3 = 0.7;
volatile float Ang_Kd3 = 0.1;
volatile float Ang_dt = 0.1;
volatile float Ang_remove = 1;

							//Speed//

							//Left Side//
int enc = 0;
int pre_enc = 0;
int enc_diff = 0;
int linear_enc = 0;
int pre_linear_enc = 0;
int dif_linear_enc = 0;
volatile float Target_Omega = 0;
volatile float Omg_Error = 0.0;
volatile float Omega = 0.0;
volatile float Omg_Error_I_Sum = 0.0;
volatile float Omega_Control = 0.0;
volatile float Omg_Kp = 1.0;
volatile float Omg_Ki = 0.00000007;
volatile float Omg_Ka;
volatile float Omg_dt = 0.01;

							//Right Side//
int enc2 = 0;
int pre_enc2 = 0;
int enc_diff2 = 0;
int linear_enc2 = 0;
int pre_linear_enc2 = 0;
int dif_linear_enc2 = 0;
volatile float Target_Omega2 = 0.0;
volatile float Omg_Error2 = 0.0;
volatile float Omega2 = 0.0;
volatile float Omg_Error_I_Sum2 = 0.0;
volatile float Omega_Control2 = 0.0;
volatile float Omg_Kp2 = 10.0;
volatile float Omg_Ki2 = 200.0;
volatile float Omg_Ka2;

							//Upper Side//
volatile float Target_Omega3 = 0.0;
volatile float Omega_ref3 = 0.0;
volatile float Omg_Error3 = 0.0;
volatile float Omega3 = 0.0;
volatile float Omg_Error_I_Sum3 = 0.0;
volatile float Omega_Control3 = 0.0;
volatile float Omg_Kp3 = 1.0;
volatile float Omg_Ki3 = 0.0000007;
volatile float Omg_Ka3;

							//Current//

							//Left Side//
volatile float Target_Current = 0;
volatile float Cur_Cur = 0.0;
volatile float Current_Ref = 0.0;
volatile float Cur_Error = 0.0;
volatile float Cur_Error_I_Sum = 0.0;
volatile float Cur_Control = 0.0;
volatile float Cur_Kp = 4.0;
volatile float Cur_Ki = 800.0;
volatile float Motor_CCR = 0.0;
volatile float dt = 0.001;
volatile float Cur_Ka;

volatile float V = 0;

							//Right Side//
volatile float Target_Current2 = 0;
volatile float Cur_Cur2 = 0.0;
volatile float Current_Ref2 = 0.0;
volatile float Cur_Error2 = 0.0;
volatile float Cur_Error_I_Sum2 = 0.0;
volatile float Cur_Control2 = 0.0;
volatile float Cur_Kp2 = 4.0;
volatile float Cur_Ki2 = 800.0;
volatile float Motor_CCR2 = 0.0;
volatile float Cur_Ka2;

							//Upper Side//
volatile float Target_Current3 = 0;
volatile float Cur_Cur3 = 0.0;
volatile float Current_Ref3 = 0.0;
volatile float Cur_Error3 = 0.0;
volatile float Cur_Error_I_Sum3 = 0.0;
volatile float Cur_Control3 = 0.0;
volatile float Cur_Kp3 = 1.0;
volatile float Cur_Ki3 = 0.3;
volatile float Motor_CCR3 = 0.0;
volatile float Cur_Ka3;
volatile float Cur_remove = 1;

int flag;

							//USART//

uint8_t Rx_data[10];					//0~5: slope 6: length 7: mode 8: pump pwm(flag) 9: stop(flag)
uint8_t Tx_data1[] = "1";
volatile float slope = 0.0;
//volatile int length;
//volatile int pump;
//volatile int mode;
//volatile int stop;
uint16_t txLen = sizeof(Tx_data1) -1;


							//Blower//

							//Pan//

/*
							//Cart handle slope - Usart2//
							//-left Motor-//

float Target_Omega(slope)
{
	float Target_L;
	if(slope > 5)
		{
		Target_L = 1;
		}
	else if(-5 <= slope <= 5)
		{
		Target_L = 2;
		}
	else if(slope < -5)
		{
		Target_L = 4;
		}
	return Target_L;
}
							//-right Motor-//
float Target_Omega2(slope)
{
	float Target_R;
	if(slope > 5)
		{
		Target_R = 4;
		}
	else if(-5 <= slope <= 5)
		{
		Target_R = 2;
		}
	else if(slope < -5)
		{
		Target_R = 1;
		}
	return Target_R;
}
*/

/*
							//Cart handle length - Usart2//
float Target_Angle(length)
{
	float Target_H;
	float Target_A;

	if(length == 1)						//camera - small -7cm
	{
		Target_H = -0.07;
	}
	else if(length == 2)				//camera - middle -15cm
	{
		Target_H = -0.15;
	}

	Target_A = Target_H * 360.0 / (2 * 0.15 * 180);		//0.3 = pully r , 1.6 = 10/ pi / 2		rad

	return Target_A;
}
*/

										//Timer//
void HAL_TIM_PeriodElapsedCallback(TIM_HandleTypeDef* htim)
{
				//Control period 1000Hz - Timer9//
	if(htim == &htim9)
	{

		HAL_ADC_Start_DMA(&hadc1, adc1_buffer, 10);

/*
		if(adc1_buffer[0] < 2600 || adc1_buffer[1] > 4000)
		{
			if(adc1_buffer[0] < 2600 && adc1_buffer[1] > 4000) 	//front resistance
			{
				process1 = 1;	//front +
			}
			else
			{
				process1 = 2;	//front one +
			}
		}
		else
		{
			process1 = 0;		//front -
		}

		if(adc1_buffer[2] < 2500 && adc1_buffer[3] > 3900)	//back resistance
		{
			process2 = 1;		//back +
		}
		else
		{
			if(adc1_buffer[2] >= 2500 && adc1_buffer[3] <= 3900)
			{
				process2 = 0;		//back -
			}
			else
			{
				process2 = 2;		//nothing
			}
		}

										//System Algorithm//

		if(process1 == 2 && process2 == 0)
		{
							//dont start keep going No controller
			a = 0;

			Target_Omega = 0;
			Target_Omega2 = 0;
			Target_Angle3 = 0;
			b_r_speed = 0;
			b_l_speed = 0;
			p_speed = 0;
			u_speed2 = 0;
		}

		if(process1 == 1 || process2 == 1)
		{
			if(process1 == 0 && process2 == 1)
			{
							//only upper dir, back pwm
				a = 1;
				Target_Omega = 0;
				Target_Omega2 = 0;
				Target_Angle3 = 0;
				b_r_speed = 672;
				b_l_speed = 700;
								//Pump Motor PWM//
				if(count_sec % 100 == 0)
				{
					p_speed = 700;
				}
			}
			else
			{
							//Controller and system on
				//camera - Target_Angle3
				Target_Angle3 = 3;
				//Delay 1s?
				Target_Omega = 4;
				Target_Omega2 = 4;

				b_r_speed = 0;
				b_l_speed = 0;
								//Pump Motor PWM//
				if(count_sec % 100 == 0)
				{
					p_speed = 700;
				}
			}
		}
		else
		{
						//system off
			Target_Omega = 0;
			Target_Omega2 = 0;
			Target_Angle3 = 0;
			u_speed2 = 0;
			b_r_speed = 0;
			b_l_speed = 0;
			p_speed = 0;
		}
*/
		Omg_Ka = 1/Omg_Kp;
		Omg_Ka2 = 1/Omg_Kp2;
		Omg_Ka3 = 1/Omg_Kp3;
		Cur_Ka = 1/Cur_Kp;
		Cur_Ka2 = 1/Cur_Kp2;
		Cur_Ka3 = 1/Cur_Kp3;

		count_sec++;

		enc3 = TIM5->CNT;			//Upper
		enc = TIM3->CNT;			//Left
		enc2 = TIM4->CNT;			//Right

 	 	 	 	 	 	 	 //Upper roller Position Controller//
		if(count_sec % 100 == 0)			//10Hz
		{


			Angle3 = linear_enc3 * 0.002416;   //rad	360 / 5200 * pi /180


			if(adc1_buffer[7] > 2500 || adc1_buffer[8] > 2500)			//psd
			{
				d = 1;
				Target_Angle3 -= 0.2;
			}

						/////
			if((Ang_Error3 > 0 && Ang_Error3 < 0.1) || (Ang_Error3 < 0 && Ang_Error3 > -0.1))
			{
				h++;
				Ang_remove = 0;
			}
			else
			{
				Ang_remove = 1;
			}
						/////

			Ang_Error3 = (Target_Angle3 - Angle3) * Ang_remove;

			Angle_Control3 = (Ang_Kp3 * Ang_Error3) + Ang_Kd3 * (Ang_Error3 - pre_Ang_Error3) * 10;		//why?? dt? Ang_dt?

			pre_Ang_Error3 = Ang_Error3;
		}


							//Speed Controller//

		if(count_sec % 10 == 0)			//100Hz
		{

							//Motor1 - Left side roller Speed//

			linear_enc = enc + dif_linear_enc;		//8? 2degree

			Omega = ((linear_enc - pre_linear_enc) * 0.895); //where dt  = 0.01 = 1ms		rad/s  445 878

			pre_linear_enc = linear_enc;

			enc_diff = enc - pre_enc;

			if(enc_diff < -60000)
			{
				i ++;
				dif_linear_enc = 65535 * i;
			}
			if(enc_diff > 60000)
			{
				i ++;
				dif_linear_enc = 65535 * (-1) * i;
			}

			pre_enc = enc;

			Omg_Error = Target_Omega - Omega;

			Omg_Error_I_Sum += Omg_Error;

			Omega_Control = Omg_Kp * Omg_Error + Omg_Ki * Omg_Error_I_Sum * dt;		//why?? Error_I_Sum

			if(Omega_Control > 1.5)
			{
				Omg_Error_I_Sum -= Omg_Ka * (Omega_Control - 1.5);
				Omega_Control = 1.5;
			}
			else if(Omega_Control < -1.5)
			{
				Omg_Error_I_Sum -= Omg_Ka * (Omega_Control + 1.5);
				Omega_Control = -1.5;
			}



							//Motor2- Right side roller Speed//

			linear_enc2 = enc2 + dif_linear_enc2;		//8? 2degree

			Omega2 = ((linear_enc2 - pre_linear_enc2) * 0.895); //where dt  = 0.01 = 1ms		rad/s 0.445	 878

			enc_diff2 = enc2 - pre_enc2;

			if(enc_diff2 < -60000)
			{

				i ++;			//different

				dif_linear_enc2 = 65535 * i;

			}

			if(enc_diff2 > 60000)
			{

				i ++;

				dif_linear_enc2 = 65535 * (-1) * i;

			}

			pre_enc2 = enc2;


			Omg_Error2 = Target_Omega2 - Omega2;

			Omg_Error_I_Sum2 += Omg_Error2;

			pre_linear_enc2 = linear_enc2;

			Omega_Control2 = Omg_Kp2 * Omg_Error2 + Omg_Ki2 * Omg_Error_I_Sum2 * dt;		//why?? Error_I_Sum


			if(Omega_Control2 > 1.5)
			{
				Omg_Error_I_Sum2 -= Omg_Ka2 * (Omega_Control2 - 1.5);
				Omega_Control2 = 1.5;
			}
			/*
			if(Omega_Control2 > 0.0)
			{
				Omg_Error_I_Sum2 -= Omg_Ka2 * (Omega_Control2);
				Omega_Control2 = 0.0;
			}*/

			else if(Omega_Control2 < -1.5)
			{
				Omg_Error_I_Sum2 -= Omg_Ka2 * (Omega_Control2 + 1.5);
				Omega_Control2 = -1.5;
			}



							//Motor3-Upper roller Speed//

			linear_enc3 = enc3 + dif_linear_enc3;		//8? 2degree			//1degree to 14.444pulse

			Omega3 = ((linear_enc3 - pre_linear_enc3) * 0.2417); //where Ang_dt  = 0.1 = 100ms		rad/s   0.2416

			enc_diff3 = enc3 - pre_enc3;

			if(enc_diff3 < -60000)
			{
				i ++;
				dif_linear_enc3 = 65535 * i;
			}
			if(enc_diff3 > 60000)
			{
				i ++;
				dif_linear_enc3 = 65535 * (-1) * i;
			}

			pre_enc3 = enc3;

			Omega_ref3 = Angle_Control3; //Angle_Control3;

			Omg_Error3 = Omega_ref3 - Omega3;

			Omg_Error_I_Sum3 += Omg_Error3;

			pre_linear_enc3 = linear_enc3;

			Omega_Control3 = Omg_Kp3 * Omg_Error3 + Omg_Ki3 * Omg_Error_I_Sum3 * dt;		//why?? Error_I_Sum

			if(Omega_Control3 > 1.0)
			{
				Omg_Error_I_Sum3 -= Omg_Ka3 * (Omega_Control3 - 1.0);
				Omega_Control3 = 1.0;
			}
			else if(Omega_Control3 < -1.0)
			{
				Omg_Error_I_Sum3 -= Omg_Ka3 * (Omega_Control3 + 1.0);
				Omega_Control3 = -1.0;
			}



		}		//if


		if(count_sec % 10 == 0)			//200Hz
		{
							//Motor1 - Left side roller Current//
			/*
			if(Target_Current2 != 0)
			{
				g_MAF_CNT2 = (g_MAF_CNT2+1)% MAF_SIZE2 ;
				g_rawData2[g_MAF_CNT2 ] = adc1_buffer[5];
				g_SUM_Data2 = 0.0;
				for(int l=0; l<MAF_SIZE2; l++)
				g_SUM_Data2 += g_rawData2[l];
				g_MAF_Data2 = g_SUM_Data2 / MAF_SIZE2;

				n = 1;
			}*/		//////////////////////
			/*
			if(Target_Omega2 != 0)
			{
				g_MAF_CNT2 = (g_MAF_CNT2+1)% MAF_SIZE2 ;
				g_rawData2[g_MAF_CNT2 ] = adc1_buffer[5];
				g_SUM_Data2 = 0.0;
				for(int l=0; l<MAF_SIZE2; l++)
				g_SUM_Data2 += g_rawData2[l];
				g_MAF_Data2 = g_SUM_Data2 / MAF_SIZE2;

				n = 1;
			}	*/	//////////////////////

			if(Target_Current3 != 0)
			{
				g_MAF_CNT3 = (g_MAF_CNT3+1)% MAF_SIZE3 ;
				g_rawData3[g_MAF_CNT3 ] = adc1_buffer[6];
				g_SUM_Data3 = 0.0;
				for(int j=0; j<MAF_SIZE3; j++)
				g_SUM_Data3 += g_rawData3[j];
				g_MAF_Data3 = g_SUM_Data3 / MAF_SIZE3;

				m = 1;
			}		//////////////////////



			if(Target_Omega != 0 && Target_Omega2 != 0)
			{
				g_MAF_CNT = (g_MAF_CNT+1)% MAF_SIZE ;
				g_rawData[g_MAF_CNT ] = adc1_buffer[4];
				g_SUM_Data = 0.0;
				for(int m=0; m<MAF_SIZE; m++)
				g_SUM_Data += g_rawData[m];
				g_MAF_Data = g_SUM_Data / MAF_SIZE;

				g_MAF_CNT2 = (g_MAF_CNT2+1)% MAF_SIZE2 ;
				g_rawData2[g_MAF_CNT2 ] = adc1_buffer[5];
				g_SUM_Data2 = 0.0;
				for(int l=0; l<MAF_SIZE2; l++)
				g_SUM_Data2 += g_rawData2[l];
				g_MAF_Data2 = g_SUM_Data2 / MAF_SIZE2;

				n = 1;
			}

			/*
			if(Target_Angle3 != 0)
			{
				g_MAF_CNT3 = (g_MAF_CNT3+1)% MAF_SIZE3 ;
				g_rawData3[g_MAF_CNT3 ] = adc1_buffer[6];
				g_SUM_Data3 = 0.0;
				for(int j=0; j<MAF_SIZE3; j++)
				g_SUM_Data3 += g_rawData3[j];
				g_MAF_Data3 = g_SUM_Data3 / MAF_SIZE3;

				m = 1;
			}*/

			Cur_Cur = (((g_MAF_Data * 3.3) / 4095.0) - 2.5 * n)/ 0.4 + 1.9 * n ;			//2.5V 400mA
			//Cur_Cur = (V - (2.5 * n)) * 10 - 0.178 ; 		//////////////////

			//Cur_Cur = ((g_MAF_Data * 3.0 / 4096.0) - (1.5 * n)); //  * 10.0;

			Current_Ref = Omega_Control; //Target_Current;				//Omega_Control;

			Cur_Error = Current_Ref - Cur_Cur;

			Cur_Error_I_Sum += Cur_Error;

			Cur_Control = (Cur_Kp * Cur_Error + Cur_Ki * Cur_Error_I_Sum * dt + 0.0153125 * Omega);

			if(Cur_Control > 12.0)
			{
				Cur_Error_I_Sum -= Cur_Ka * (Cur_Control - 12.0);
				Cur_Control = 12.0;
			}
			else if(Cur_Control < 0.0)
			{
				Cur_Error_I_Sum -= Cur_Ka * (Cur_Control);
				Cur_Control = 0.0;
			}

			Motor_CCR = Cur_Control;
			f_l_speed = Motor_CCR * 1000 / 12;
			//TIM1->CCR1 = f_l_speed;							//left motor


							//Motor2 - Right side roller Current//

			Cur_Cur2 = (((-1) * (g_MAF_Data2 * 3.3) / 4095.0) + 2.5 * n)/ 0.4 - 0.1 * n; // + 0.3 * n;			//2.5V 400mA

			//Cur_Cur2 = ((g_MAF_Data2 - 2048.0 * n) * 3.3) / 4095.0/ 0.4;			//400mA

			//Cur_Cur2 = ((g_MAF_Data2 * 3.0 / 4096.0) - (2.3 * n)); //  * 10.0;

			Current_Ref2 = Omega_Control2;			//Omega_Control2	//Target_Current2

			Cur_Error2 = Current_Ref2 - Cur_Cur2;

			Cur_Error_I_Sum2 += Cur_Error2;

			Cur_Control2 = Cur_Kp2 * Cur_Error2 + Cur_Ki2 * Cur_Error_I_Sum2 * dt + 0.0153125 * Omega2;

			if(Cur_Control2 > 0.0)
			{
				Cur_Error_I_Sum2 -= Cur_Ka2 * (Cur_Control2);
				Cur_Control2 = 0.0;
			}
			else if(Cur_Control2 < -12.0)
			{
				Cur_Error_I_Sum2 -= Cur_Ka2 * (Cur_Control2 + 12.0);
				Cur_Control2 = -12.0;
			}

			Motor_CCR2 = Cur_Control2;
			f_r_speed = Motor_CCR2 * 1000 / 12;
			//TIM1->CCR2 = f_r_speed;



							//Motor3 - Upper roller Current//

			if(Ang_Error3 == 0)
			{
				Cur_remove = 0;
			}
			else
			{
				Cur_remove = 1;
			}

			Cur_Cur3 = (((g_MAF_Data3 * 3.3) / 4095.0) - 2.5 * n)/ 0.4;			//2.5V 400mA

			//Cur_Cur3 = ((g_MAF_Data3 - 2048.0 * m) * 3.3) / 4095.0/ 0.4;			//400mA

			//Cur_Cur3 = ((g_MAF_Data3 * 3.0 / 4096.0) - (1.55 * m)); // * 10.0;

			Current_Ref3 = Target_Current3;				//Omega_Control3 //Target_Current3

			Cur_Error3 = (Current_Ref3 - Cur_Cur3) * Cur_remove;

			Cur_Error_I_Sum3 += Cur_Error3;

			Cur_Control3 = Cur_Kp3 * Cur_Error3 + Cur_Ki3 * Cur_Error_I_Sum3 * dt + 0.0153125 * Omega3;

			if(Cur_Control3 > 12.0)
			{
				Cur_Error_I_Sum3 -= Cur_Ka3 * (Cur_Control3 - 12.0);
				Cur_Control3 = 12.0;
			}
			else if(Cur_Control3 < -12.0)
			{
				Cur_Error_I_Sum3 -= Cur_Ka3 * (Cur_Control3 + 12.0);
				Cur_Control3 = -12.0;
			}

			Motor_CCR3 = Cur_Control3;
			u_speed = Motor_CCR3 * 1000 / 12;
			TIM1->CCR3 = u_speed;
		}



						//Motor rotation direction//

		//a = HAL_GPIO_ReadPin(GPIOB, GPIO_PIN_12);
		b = HAL_GPIO_ReadPin(GPIOB, GPIO_PIN_13);
		c = HAL_GPIO_ReadPin(GPIOB, GPIO_PIN_14);
		d = HAL_GPIO_ReadPin(GPIOB, GPIO_PIN_15);

		if(a == 0)
		{
		  HAL_GPIO_WritePin(GPIOC, GPIO_PIN_12, 0);			//u2
		}
		else if(a == 1)
		{
		  HAL_GPIO_WritePin(GPIOC, GPIO_PIN_12, 1);
		}

		if(b == 0)
		{
		  HAL_GPIO_WritePin(GPIOC, GPIO_PIN_13, 1);			//f_l
		}
		else if(b == 1)
		{
		  HAL_GPIO_WritePin(GPIOC, GPIO_PIN_13, 0);
		}

		if(c == 0)
		{
		  HAL_GPIO_WritePin(GPIOC, GPIO_PIN_14, 0);			//f_r
		}
		else if(c == 1)
		{
		  HAL_GPIO_WritePin(GPIOC, GPIO_PIN_14, 1);
		}

		if(d == 0)
		{
		  HAL_GPIO_WritePin(GPIOC, GPIO_PIN_15, 1);			//u
		}
		else if(d == 1)
		{
		  HAL_GPIO_WritePin(GPIOC, GPIO_PIN_15, 0);
		}
	}

	/*
	if(flag == 2)
	{
		Omg_Error_I_Sum = 0;
		Cur_Error_I_Sum = 0;
		Omg_Error_I_Sum2 = 0;
		Cur_Error_I_Sum2 = 0;
		Omg_Error_I_Sum3 = 0;
		Cur_Error_I_Sum3 = 0;
		Cur_Error3 = 0;
		Omg_Error3 = 0;
	}*/

							//just pwm //

	//TIM1->CCR1 = f_l_speed;
	//TIM1->CCR2 = f_r_speed;

	TIM8->CCR1 = b_l_speed;
	TIM8->CCR2 = b_r_speed;
	TIM8->CCR3 = u_speed2;
	TIM8->CCR4 = p_speed;

}

/* USER CODE END 0 */

/**
  * @brief  The application entry point.
  * @retval int
  */
int main(void)
{
  /* USER CODE BEGIN 1 */

  /* USER CODE END 1 */

  /* MCU Configuration--------------------------------------------------------*/

  /* Reset of all peripherals, Initializes the Flash interface and the Systick. */
  HAL_Init();

  /* USER CODE BEGIN Init */

  /* USER CODE END Init */

  /* Configure the system clock */
  SystemClock_Config();

  /* USER CODE BEGIN SysInit */

  /* USER CODE END SysInit */

  /* Initialize all configured peripherals */
  MX_GPIO_Init();
  MX_DMA_Init();
  MX_ADC1_Init();
  MX_TIM1_Init();
  MX_TIM2_Init();
  MX_TIM3_Init();
  MX_TIM4_Init();
  MX_TIM8_Init();
  MX_USART2_UART_Init();
  MX_TIM5_Init();
  MX_TIM9_Init();
  /* USER CODE BEGIN 2 */

  HAL_UART_Receive_IT(&huart2, (uint8_t*)Rx_data, 10);

  HAL_TIM_PWM_Start(&htim1, TIM_CHANNEL_1);
  HAL_TIM_PWM_Start(&htim1, TIM_CHANNEL_2);
  HAL_TIM_PWM_Start(&htim1, TIM_CHANNEL_3);

  HAL_TIM_PWM_Start(&htim8, TIM_CHANNEL_1);
  HAL_TIM_PWM_Start(&htim8, TIM_CHANNEL_2);
  HAL_TIM_PWM_Start(&htim8, TIM_CHANNEL_3);
  HAL_TIM_PWM_Start(&htim8, TIM_CHANNEL_4);

  HAL_TIM_Encoder_Start(&htim3, TIM_CHANNEL_ALL);
  HAL_TIM_Encoder_Start(&htim4, TIM_CHANNEL_ALL);
  HAL_TIM_Encoder_Start(&htim5, TIM_CHANNEL_ALL);

  HAL_TIM_Base_Start_IT(&htim2);			//ADC
  HAL_TIM_Base_Start_IT(&htim9);			//Controller

  /* USER CODE END 2 */

  /* Infinite loop */
  /* USER CODE BEGIN WHILE */
  while (1)
  {
    /* USER CODE END WHILE */

    /* USER CODE BEGIN 3 */

  }
  /* USER CODE END 3 */
}

/**
  * @brief System Clock Configuration
  * @retval None
  */
void SystemClock_Config(void)
{
  RCC_OscInitTypeDef RCC_OscInitStruct = {0};
  RCC_ClkInitTypeDef RCC_ClkInitStruct = {0};

  /** Configure the main internal regulator output voltage
  */
  __HAL_RCC_PWR_CLK_ENABLE();
  __HAL_PWR_VOLTAGESCALING_CONFIG(PWR_REGULATOR_VOLTAGE_SCALE1);
  /** Initializes the RCC Oscillators according to the specified parameters
  * in the RCC_OscInitTypeDef structure.
  */
  RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSI;
  RCC_OscInitStruct.HSIState = RCC_HSI_ON;
  RCC_OscInitStruct.HSICalibrationValue = RCC_HSICALIBRATION_DEFAULT;
  RCC_OscInitStruct.PLL.PLLState = RCC_PLL_ON;
  RCC_OscInitStruct.PLL.PLLSource = RCC_PLLSOURCE_HSI;
  RCC_OscInitStruct.PLL.PLLM = 8;
  RCC_OscInitStruct.PLL.PLLN = 180;
  RCC_OscInitStruct.PLL.PLLP = RCC_PLLP_DIV2;
  RCC_OscInitStruct.PLL.PLLQ = 2;
  RCC_OscInitStruct.PLL.PLLR = 2;
  if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK)
  {
    Error_Handler();
  }
  /** Activate the Over-Drive mode
  */
  if (HAL_PWREx_EnableOverDrive() != HAL_OK)
  {
    Error_Handler();
  }
  /** Initializes the CPU, AHB and APB buses clocks
  */
  RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK|RCC_CLOCKTYPE_SYSCLK
                              |RCC_CLOCKTYPE_PCLK1|RCC_CLOCKTYPE_PCLK2;
  RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_PLLCLK;
  RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;
  RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV4;
  RCC_ClkInitStruct.APB2CLKDivider = RCC_HCLK_DIV2;

  if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_5) != HAL_OK)
  {
    Error_Handler();
  }
}

/* USER CODE BEGIN 4 */

void HAL_UART_RxCpltCallback(UART_HandleTypeDef * huart)
{
	HAL_UART_Transmit(&huart2, (uint8_t*)Tx_data1, txLen,10);
	slope = atof(Rx_data);			//-180~+180 degree
	HAL_UART_Receive_IT(&huart2, (uint8_t*)Rx_data, 10);
}

/* USER CODE END 4 */

/**
  * @brief  This function is executed in case of error occurrence.
  * @retval None
  */
void Error_Handler(void)
{
  /* USER CODE BEGIN Error_Handler_Debug */
  /* User can add his own implementation to report the HAL error return state */
  __disable_irq();
  while (1)
  {
  }
  /* USER CODE END Error_Handler_Debug */
}

#ifdef  USE_FULL_ASSERT
/**
  * @brief  Reports the name of the source file and the source line number
  *         where the assert_param error has occurred.
  * @param  file: pointer to the source file name
  * @param  line: assert_param error line source number
  * @retval None
  */
void assert_failed(uint8_t *file, uint32_t line)
{
  /* USER CODE BEGIN 6 */
  /* User can add his own implementation to report the file name and line number,
     ex: printf("Wrong parameters value: file %s on line %d\r\n", file, line) */
  /* USER CODE END 6 */
}
#endif /* USE_FULL_ASSERT */

/************************ (C) COPYRIGHT STMicroelectronics *****END OF FILE****/
