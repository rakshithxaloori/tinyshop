"use client";
import React, { use, useCallback, useEffect, useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { Button } from "@/components/ui/button";
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Checkbox } from "@/components/ui/checkbox";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import { indianSubcontinentCountries, indianStatesAndUTs } from "@/components/countries";
import { cn } from '@/lib/utils';
import { CustomerSession } from '@/types/session';
import useCartStore from '@/store/cart';
import { Checkout } from '@tinyshop/tinyshop-node/interfaces/checkout';
import { createCheckout, createCustomerAddress, deleteCheckout, updateCheckout, updateCustomerDetails } from '@/lib/checkout';
import { CustomerAddressCreate } from '@tinyshop/tinyshop-node/interfaces/customerAddress';

declare global {
  interface Window {
    Razorpay: any;
  }
}

const formSchema = z.object({
  email: z.string().email(),
  fullName: z.string().min(2, "Full name must be at least 2 characters"),
  country: z.string(),
  addressLine1: z.string(),
  addressLine2: z.string().optional(),
  city: z.string(),
  pin: z.string(),
  state: z.string(),
  phoneNumber: z.string(),
  sameAsBilling: z.boolean(),
  billingAddressLine1: z.string().optional(),
  billingAddressLine2: z.string().optional(),
  billingCity: z.string().optional(),
  billingPin: z.string().optional(),
  billingState: z.string().optional(),
});

const CheckoutForm = ({
  session,
  className }: {
    session: CustomerSession | null,
    className?: string
  }) => {
  const customerId = session?.customerId
  const cartId = useCartStore(state => state.id);
  const [checkout, setCheckout] = useState<Checkout | null>(null);
  const [blurredFields, setBlurredFields] = useState({ email: false, fullName: false });
  const [shouldUpdateCustomer, setShouldUpdateCustomer] = useState(false);

  const phone = session?.phone || '';
  const form = useForm({
    resolver: zodResolver(formSchema),
    defaultValues: {
      email: '',
      fullName: '',
      country: 'India',
      addressLine1: '',
      addressLine2: '',
      city: '',
      pin: '',
      state: '',
      phoneNumber: phone,
      sameAsBilling: true,
      billingAddressLine1: '',
      billingAddressLine2: '',
      billingCity: '',
      billingPin: '',
      billingState: '',
    },
  });

  const handleBlur = useCallback((fieldName: string) => {
    setBlurredFields((prev) => {
      const newState = { ...prev, [fieldName]: true };
      return newState;
    });
  }, []);

  useEffect(() => {
    if (blurredFields.email && blurredFields.fullName && customerId) {
      setShouldUpdateCustomer(true);
    }
  }, [blurredFields, customerId]);

  useEffect(() => {
    if (!customerId || !shouldUpdateCustomer)
      return;

    (async () => {
      try {
        const updatedCustomer = await updateCustomerDetails(customerId, {
          email: form.getValues('email'),
          name: form.getValues('fullName')
        });
      } catch (error) {
        console.error('Failed to update customer details:', error);
      } finally {
        setShouldUpdateCustomer(false);
      }
    })();
  }, [shouldUpdateCustomer, customerId, form]);

  useEffect(() => {
    const auth = !!customerId;
    let newCheckout: Checkout | null = null;

    async function createCheckoutObject() {
      if (auth && cartId) {
        // create a checkout object
        newCheckout = await createCheckout(cartId, customerId);
        setCheckout(newCheckout);
      }
    }
    createCheckoutObject();

    return () => {
      if (newCheckout) {
        (async () => {
          // delete the checkout object
          await deleteCheckout(newCheckout.id);
        })(); // Immediately invoke the async function
      }
    }
  }, [customerId, cartId]);

  useEffect(() => {
    const script = document.createElement('script');
    script.src = 'https://checkout.razorpay.com/v1/checkout.js';
    script.async = true;
    document.body.appendChild(script);

    return () => {
      document.body.removeChild(script);
    };
  }, []);

  const openRazorpay = ({ name, email, contact, tinyshopSubscriptionId, providerSubscriptionId }: {
    name: string;
    email: string;
    contact: string;
    tinyshopSubscriptionId: string;
    providerSubscriptionId: string;
  }) => {
    const options = {
      key: process.env.NEXT_PUBLIC_RAZORPAY_KEY_ID,
      name: process.env.NEXT_PUBLIC_SHOP_NAME,
      description: "Test Transaction",
      callback_url: `${process.env.NEXT_PUBLIC_BASE_URL}/razorpay?subId=${tinyshopSubscriptionId}`,
      subscription_id: providerSubscriptionId,
      prefill: {
        name: name,
        email: email,
        contact: contact
      },
      notes: {
        address: "Razorpay Corporate Office"
      },
      recurring: true,
      send_sms_hash: true,
      readonly: {
        name: true,
        email: true,
        contact: true
      },
      theme: {
        color: "#3399cc"
      }
    };

    const rzp1 = new window.Razorpay(options);
    rzp1.open();
  };

  const onSubmit = async (data: z.infer<typeof formSchema>) => {
    // Handle form submission
    if (!customerId || !checkout)
      return;

    // console.log("form data", data);
    const customerAddressObject: CustomerAddressCreate = {
      customer: customerId,
      name: "Home",
      line1: data.addressLine1,
      city: data.city,
      state: data.state,
      country: data.country.slice(0, 2).toUpperCase(),
      postal_code: data.pin,
    }

    if (data.addressLine2) {
      customerAddressObject.line2 = data.addressLine2;
    }

    const customerAddress = await createCustomerAddress(customerAddressObject);

    const updatedCheckout = await updateCheckout(checkout.id, 'processing', customerAddress.id);

    openRazorpay({
      name: data.fullName,
      email: data.email,
      contact: `+91${phone}`,
      tinyshopSubscriptionId: updatedCheckout.subscriptions?.data[0].id || '',
      providerSubscriptionId: updatedCheckout.subscriptions?.data[0].provider_details.razorpay?.subscription_id || ''
    });
  };

  return (
    <Card className={cn("max-w-2xl my-lg mx-auto mt-8 bg-base-200 text-nuetral-content", className)}>
      <CardHeader>
        <CardTitle>Checkout</CardTitle>
        <CardDescription>Provide billing and shipping details below.</CardDescription>
      </CardHeader>
      <CardContent>
        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
            <FormField
              control={form.control}
              name="email"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Email</FormLabel>
                  <FormControl>
                    <Input placeholder="Email address" {...field}
                      onBlur={() => {
                        field.onBlur();
                        handleBlur('email');
                      }}
                    />
                  </FormControl>
                  <FormMessage className='text-error' />
                </FormItem>
              )}
            />
            <FormField
              control={form.control}
              name="fullName"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Full name</FormLabel>
                  <FormControl>
                    <Input placeholder="First and last name" {...field}
                      onBlur={() => {
                        field.onBlur();
                        handleBlur('fullName');
                      }}
                    />
                  </FormControl>
                  <FormMessage className='text-error' />
                </FormItem>
              )}
            />
            <FormField
              control={form.control}
              name="country"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Country or region</FormLabel>
                  <Select onValueChange={field.onChange} defaultValue={field.value}>
                    <FormControl>
                      <SelectTrigger>
                        <SelectValue placeholder="Select a country" />
                      </SelectTrigger>
                    </FormControl>
                    <SelectContent>
                      {
                        indianSubcontinentCountries.map((country) => (
                          <SelectItem key={country.code} value={country.name}>
                            {country.flag} {"  "} {country.name}
                          </SelectItem>
                        ))
                      }
                    </SelectContent>
                  </Select>
                  <FormMessage />
                </FormItem>
              )}
            />
            <FormField
              control={form.control}
              name="addressLine1"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Address line 1</FormLabel>
                  <FormControl>
                    <Input placeholder="Street address" {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <FormField
              control={form.control}
              name="addressLine2"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Address line 2</FormLabel>
                  <FormControl>
                    <Input placeholder="Apt., suite, unit number, etc. (optional)" {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <FormField
              control={form.control}
              name="city"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>City</FormLabel>
                  <FormControl>
                    <Input {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <div className="grid grid-cols-2 gap-4">
              <FormField
                control={form.control}
                name="pin"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>PIN</FormLabel>
                    <FormControl>
                      <Input {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <FormField
                control={form.control}
                name="state"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>State</FormLabel>
                    <Select onValueChange={field.onChange} defaultValue={field.value}>
                      <FormControl>
                        <SelectTrigger>
                          <SelectValue placeholder="Select a state" />
                        </SelectTrigger>
                      </FormControl>
                      <SelectContent>
                        {/* Create a group of Indian states */}

                        {
                          indianStatesAndUTs.states.map((state) => (
                            <SelectItem key={state} value={state}>
                              {state}
                            </SelectItem>
                          ))
                        }
                        {/* Add more state options */}
                      </SelectContent>
                    </Select>
                    <FormMessage />
                  </FormItem>
                )}
              />
            </div>
            <FormField
              control={form.control}
              name="phoneNumber"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Phone number</FormLabel>
                  <FormControl>
                    <div className="flex">
                      <span className="inline-flex items-center px-3 rounded-l-md border border-r-0 border-gray-300 bg-gray-50 text-gray-500 text-sm">
                        +91
                      </span>
                      <Input className="rounded-l-none" {...field} value={phone} disabled />
                    </div>
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <FormField
              control={form.control}
              name="sameAsBilling"
              render={({ field }) => (
                <FormItem className="flex flex-row items-start space-x-3 space-y-0">
                  <FormControl>
                    <Checkbox
                      checked={field.value}
                      onCheckedChange={field.onChange}
                    />
                  </FormControl>
                  <div className="space-y-1 leading-none">
                    <FormLabel>
                      Billing address same as shipping
                    </FormLabel>
                  </div>
                </FormItem>
              )}
            />
            {!form.watch('sameAsBilling') && (
              <>
                <h2 className="text-xl font-semibold mt-6 mb-4">Billing Address</h2>
                <FormField
                  control={form.control}
                  name="billingAddressLine1"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Address</FormLabel>
                      <FormControl>
                        <Input placeholder="Street address" {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
                <FormField
                  control={form.control}
                  name="billingAddressLine2"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Address (cont.)</FormLabel>
                      <FormControl>
                        <Input placeholder="Apt., suite, unit number, etc. (optional)" {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
                <FormField
                  control={form.control}
                  name="billingCity"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>City</FormLabel>
                      <FormControl>
                        <Input {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
                <div className="grid grid-cols-2 gap-4">
                  <FormField
                    control={form.control}
                    name="billingPin"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>PIN</FormLabel>
                        <FormControl>
                          <Input {...field} />
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                  <FormField
                    control={form.control}
                    name="billingState"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>State</FormLabel>
                        <Select onValueChange={field.onChange} defaultValue={field.value}>
                          <FormControl>
                            <SelectTrigger>
                              <SelectValue placeholder="Select a state" />
                            </SelectTrigger>
                          </FormControl>
                          <SelectContent>
                            {/* Create a group of Indian states */}
                            {
                              indianStatesAndUTs.states.map((state) => (
                                <SelectItem key={state} value={state}>
                                  {state}
                                </SelectItem>
                              ))
                            }
                            {/* Add more state options */}
                          </SelectContent>
                        </Select>
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                </div>
              </>
            )}
            <Button type="submit" className="w-full">Submit</Button>
          </form>
        </Form>
      </CardContent>
    </Card>
  );
};

export default CheckoutForm;