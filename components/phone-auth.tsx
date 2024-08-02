"use client"
import { cn } from "@/lib/utils"
import React, { useState } from 'react';
import { z } from 'zod';
import { Input } from "./ui/input";
import { Button } from "./ui/button";
import { InputOTP, InputOTPGroup, InputOTPSlot } from './ui/input-otp'
import { PencilIcon } from "lucide-react";
import { sendCustomerOtp, signInCustomer, verifyCustomerOtp } from "@/lib/server-actions";

const phoneSchema = z.string().regex(/^[6-9]\d{9}$/, 'Invalid phone number');
const otpSchema = z.string().length(6, 'OTP must be 6 digits');


const PhoneNumberInput = ({ phone, setPhone, error, handlePhoneSubmit }: {
  phone: string, setPhone: any, error: string,
  handlePhoneSubmit: (e: any) => void
}) => {
  return (
    <form onSubmit={handlePhoneSubmit}>
      <div className="mb-md text-lg font-semibold">Enter your phone number</div>
      <div className="flex flex-row items-center">
        <div className="flex h-10 items-center flex-row px-sm gap-1 border-2 border-r-0 border-primary border-r-none rounded-l-lg bg-base-200">
          <span >🇮🇳</span>
          <span >+91</span>
        </div>
        <Input
          type="tel"
          className="rounded-l-none border-2 border-l-0 border-primary text-primary-content focus-visible:ring-0 focus-visible:ring-offset-0 w-fit"
          value={phone}
          onChange={(e) => setPhone(e.target.value)}
          placeholder=""
        />
      </div>
      <p className="text-error my-sm">{error || ""}</p>
      <Button className="mt-sm text-primary-content" type="submit">Continue</Button>
    </form>
  )
}

const VerifyOTP = ({ otp, setOtp, error, handleOtpSubmit, handlePhoneChange }: {
  otp: string, setOtp: any, error: string,
  handleOtpSubmit: (e: any) => void;
  handlePhoneChange: () => void;
}) => {
  return (
    <form onSubmit={handleOtpSubmit}>
      <div className="text-lg font-semibold">Enter OTP sent to your phone</div>
      <Button variant="link" className="text-primary-content p-0 mt-0 mb-md h-fit" onClick={handlePhoneChange}>
        <PencilIcon className="h-3 w-3 mr-sm" /> {" Edit number"}
      </Button>
      <InputOTP maxLength={6} value={otp}
        onChange={(value: any) => setOtp(value)}
      >
        <InputOTPGroup>
          <InputOTPSlot index={0} />
          <InputOTPSlot index={1} />
          <InputOTPSlot index={2} />
          <InputOTPSlot index={3} />
          <InputOTPSlot index={4} />
          <InputOTPSlot index={5} />
        </InputOTPGroup>
      </InputOTP>
      <p className="text-error my-sm">{error || ""}</p>
      <Button className="mt-sm text-primary-content" type="submit">Verify</Button>
    </form>
  )
}

const PhoneAuth = ({ className }: { className?: string }) => {
  const [step, setStep] = useState(1);
  const [phone, setPhone] = useState('');
  const [otp, setOtp] = useState('');
  const [error, setError] = useState('');
  const [customerId, setCustomerId] = useState<string | null>(null);

  const handlePhoneSubmit = (e: any) => {
    e.preventDefault();
    try {
      phoneSchema.parse(phone);
      // Mock function to send OTP
      const phoneNum = `+91${phone}`;
      sendOTP(phoneNum);
      setStep(2);
      setError('');
    } catch (err: any) {
      setError(err.errors[0].message);
    }
  };

  const handleOtpSubmit = async (e: any) => {
    e.preventDefault();
    try {
      otpSchema.parse(otp);
      // Mock function to verify OTP
      const isValid = await verifyOTP(otp);
      if (isValid) {
        await signInCustomer(customerId!, phone);
        setError('');
      } else {
        throw new Error('Invalid OTP');
      }
    } catch (err: any) {
      if (err instanceof z.ZodError) {
        const errorMessage = err.errors[0].message;
        setError(errorMessage);
      }
      setOtp('');
    }
  };

  // Mock functions for OTP operations
  const sendOTP = async (phone: string) => {
    const { id } = await sendCustomerOtp(phone);
    setCustomerId(id);
  };

  const verifyOTP = async (otp: string) => {
    // For demonstration, let's say OTP '123456' is always correct
    const { verified } = await verifyCustomerOtp(customerId!, otp);
    return verified;
  };

  return (
    <div className={cn("my-lg  rounded-xl h-fit", className)}>
      {step === 1 && (
        <PhoneNumberInput
          phone={phone}
          setPhone={setPhone}
          error={error}
          handlePhoneSubmit={handlePhoneSubmit}
        />
      )}

      {step === 2 && (
        <VerifyOTP
          otp={otp}
          setOtp={setOtp}
          error={error}
          handleOtpSubmit={handleOtpSubmit}
          handlePhoneChange={() => setStep(1)}
        />
      )}
    </div>
  );
};

export default PhoneAuth