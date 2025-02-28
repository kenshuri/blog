---
title: Manage authentification with Django-Ninja and NextJS
summary: Implement a full authentification mecanism between your Django-Ninja API and NextJS v15 Frontend using JWT and Auth.JS v5
date: 2030-12-09
badge: code
image:
---

# Manage authentification with Django-Ninja and NextJS

When building modern web applications, managing authentication is a critical piece of the puzzle. In this post, we’ll explore how to implement a robust authentication mechanism for your project using Django-Ninja as the backend and Next.js for the frontend. By leveraging JWT (JSON Web Tokens) and the versatile Auth.js library, you'll learn how to seamlessly connect these technologies for secure and efficient user authentication. Whether you’re a beginner or looking to refine your approach, this guide will provide practical steps and insights to get you started. Let’s dive in!

## Django-Ninja API

## Front-end

### Presentation

#### Next.js Framework
Next.js is a popular React-based framework known for its powerful features like server-side rendering (SSR), static site generation (SSG), and seamless API routes. It provides a developer-friendly environment for building high-performance, scalable web applications. With its flexibility and rich ecosystem, Next.js is a great choice for integrating modern authentication flows.

#### Auth.js
Auth.js (formerly NextAuth.js) is a flexible and easy-to-use library for handling authentication in Next.js applications. It supports a variety of authentication strategies, including OAuth, email/password, and JWT. With minimal configuration, you can implement secure login flows and integrate third-party providers like Google, GitHub, and more. Its modularity makes it an excellent fit for projects where customization and security are top priorities.

#### Why Use Auth.js for Authentication?
While we could implement the entire authentication mechanism ourselves, we’ll rely on Auth.js to simplify the process. Auth.js will manage the session lifecycle for us, while we’ll use the JWT tokens provided by our Django backend to authenticate API requests.

#### Understanding Auth.js’s Role in the Authentication Process
When I first started working with Auth.js, I assumed it would handle backend tokens seamlessly, much like it manages authentication with third-party providers. However, I quickly realized that’s not the case.

Auth.js is primarily a session management library. Its job is to help you manage user sessions by storing session data in a cookie and providing tools to manage the session lifecycle. What you choose to store in that session cookie is entirely up to you. In our case, we’ll store the access and refresh tokens from our Django backend, which are necessary for making authenticated requests.

#### Clearing Up the JWT Confusion (many thanks to [you](https://sourcehawk.medium.com/next-auth-with-a-custom-authentication-backend-12c8f54ed4ce))
One thing that initially tripped me up was Auth.js’s use of the term “JWT” to describe the cookie it manages for you. This can be misleading because the JWT tokens from your backend—such as the access token and refresh token—are entirely separate from the JWT session cookie managed by Auth.js.

To clarify:

- The JWT session cookie in Auth.js is what it uses to store and manage session data.
- The JWT tokens from your backend (access and refresh tokens) need to be explicitly stored in this session cookie so they can be used to authenticate requests to the backend.
This distinction is crucial as we move forward with the implementation. Keep it in mind as we dive deeper into integrating Django-Ninja and Next.js with Auth.js!

#### Get the Right Tools
To interact with our API, we will use Postman as the testing tool. Ensure that you have Postman installed and ready for making requests.

### Testing API for Token & User Data

We will test the API to retrieve both a user token and user information. Here's an example of the response you should expect:
```json
{
    "email": "your@email.com",
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczMzg0MDk0OSwiaWF0IjoxNzMzNzU0NTQ5LCJqdGkiOiJmOGFkMTdiMGY3OGI0NDE1YjIzNzIzYmVlNjdjNTFkNiIsInVzZXJfaWQiOjF9.2afjXjZ2VGWHRmTFjwZFgUOmrFpi-wXpePX-FTTsvN8",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzMzNzU4MTQ5LCJpYXQiOjE3MzM3NTQ1NDksImp0aSI6IjZiNDhlNTFhYTZmMTRlMDY5NTJlZGYzZWUzODc2MDA1IiwidXNlcl9pZCI6MX0.-40ccGdTjEl2Lfzt7ocPS-jvu4T7akfaIthzwtJ-NU0"
}
```

#### Response Breakdown

- **`email`**: The email address associated with the user.
- **`refresh`**: A long-lived token used to obtain a new access token when the current one expires.
- **`access`**: A short-lived token used to authenticate API requests.

#### Steps to Test

1. **Open Postman** and create a new request.
2. **Configure the request method** (e.g., `POST` or `GET`) and the API endpoint.
3. **Provide necessary headers** (e.g., `Content-Type: application/json`) and body data.
4. **Send the request** and verify the response.


### Accessing Authenticated Endpoint

Now, using the `accessToken` received in the previous part, we can try to access an endpoint that requires authentication.

If you try it without changing anything, you should receive a `401` HTTP code with a body indicating that the request is unauthorized.

```json
{
    "detail": "Unauthorized"
}
```


#### Adding the Token

To resolve this, we need to add the token to the request. In **Postman**, follow these steps:

1. Go to the **Authorization** tab.
2. Select **Bearer Token** as the type.
3. Paste the `accessToken` you obtained in the previous part.

After adding the token, send the request again. You should receive a `200` HTTP code with a successful response body.

```json
{
    "id": 1,
    "display_username": "username",
    "unique_username": "username",
    "email": "your@email.com",
    "is_authenticated": true
}
```

The key question now is:  
> How can we access and store this token and user information in our Next.js application?

### Install Auth.js - Previously NextAuth

Install the latest version of Auth.js following doc on the [official website](https://authjs.dev/getting-started/installation?framework=Next.js). 

Now I expect you followed everything. You should thus have a file auth.ts at the root of your app (in the `src` folder).

Next step is to configure your credential provider so that it works with the JWT token sent by your backend.

### Setting-up the credentials provider

Now, we'll need to follow several steps:

- Modify Auth.js to add the credential provider
- Create the login component
- Create a new login page
- Check that it worked by accessing the session data: need to wrap in the session provider

#### Add Credential provider to your `auth.ts`

The changes to the auth.ts file involve the addition of a Credential Provider and supporting configurations to enable authentication using user-provided email and password credentials. Here's a breakdown of what changed and why:

##### Before

###### src/auth.ts
```typescript
import NextAuth from "next-auth"
 
export const { handlers, signIn, signOut, auth } = NextAuth({
  providers: [],
})
```

- The initial implementation of NextAuth had an empty providers array, meaning no authentication methods were defined.
- It only exported the essential handlers (handlers, signIn, signOut, and auth) without specifying any mechanism for how users would authenticate.

##### After

###### src/auth.ts
```typescript
import NextAuth from "next-auth"
import Credentials from "next-auth/providers/credentials"
import axios from "axios";
import {DJANGO_API_URL} from "@/config/defaults";

export const { handlers, signIn, signOut, auth } = NextAuth({
    providers: [
        Credentials({
            // You can specify which fields should be submitted, by adding keys to the `credentials` object.
            // e.g. domain, username, password, 2FA token, etc.
            credentials: {
                email: {},
                password: {},
            },
            authorize: async (credentials) => {
                try {
                    const response = await axios.post(`${DJANGO_API_URL}/token/pair`, {
                        email: credentials.email,
                        password: credentials.password,
                    });

                    const user = response.data;

                    if (!user || !user.email) {
                        throw new Error("Invalid credentials.");
                    }
                    
                    
                    // Return user object with their profile data
                    console.log("The user being returned: ", user)
                    return user;
                } catch (error) {
                    console.error("Error during authentication:", error);
                    throw new Error("Authentication failed. Please check your credentials.");
                }
            },
        }),
    ],
})
```

1. Added Credentials Provider:
   - The Credentials provider allows users to authenticate using their email and password.
   - This setup customizes the login flow by defining a credentials object containing the expected fields (email and password) and an authorize function that validates the user.
2. Imported axios:
   - The axios library is used for making HTTP POST requests to the Django API (/token/pair) to validate user credentials.
3. Integration with Django API:
   - The authorize function sends the provided email and password to the Django API (DJANGO_API_URL/token/pair) for validation.
   - If the API returns a valid user, the user object is passed to NextAuth, enabling subsequent authentication flows.
   - If validation fails (e.g., wrong password), an error is thrown, stopping the authentication process.
4. Error Handling:
   - Added comprehensive error handling to manage scenarios like invalid credentials or API errors.
   - Logs any errors during the authentication process for debugging.
   - We will change this process in a latter part.
5. Dynamic Configuration:
   - The API URL (DJANGO_API_URL) is dynamically imported from the configuration, making the setup environment-agnostic and easier to manage.

### Create a SignIn form

You can create a simple signin form to get credentials from the user. The given code implements a simple client-side sign-in form for a Next.js application, leveraging the Credentials Provider defined earlier. 

###### src/components/auth/sign-in.tsx
```typescript jsx
"use client"
import { signIn } from "next-auth/react"

export function SignIn() {
    const credentialsAction = (event) => {
        event.preventDefault(); // Prevent the default form submission behavior
        const formData = new FormData(event.target); // Create a FormData object from the form
        const data = Object.fromEntries(formData.entries()); // Convert FormData to a plain object

        // Call the signIn function with the credentials provider
        signIn("credentials", {
            email: data.email,
            password: data.password,
            redirect: false, // Optionally disable automatic redirects
        });
    };

    return (
        <form onSubmit={credentialsAction}>
            <label htmlFor="credentials-email">
                Email
                <input type="email" id="credentials-email" name="email" />
            </label>
            <label htmlFor="credentials-password">
                Password
                <input type="password" id="credentials-password" name="password" />
            </label>
            <input type="submit" value="Sign In" />
        </form>
    )
}
```

The `SignIn` component is a simple client-side form for signing in using the Credentials Provider from NextAuth.

#### Key Features

1. **Client-Side Authentication**:
   - The `signIn` function from `next-auth/react` is used to authenticate with the Credentials Provider.

2. **Custom Form Handling**:
   - The `credentialsAction` function handles the form submission:
     - **`event.preventDefault()`**: Prevents default page reload.
     - **`FormData`**: Extracts form input values.
     - **`signIn`**: Sends credentials (`email` and `password`) to the provider.

3. **Controlled Navigation**:
   - The `redirect: false` option prevents automatic redirection, allowing for custom handling of success or failure.


#### Code Flow

1. **Form Submission**:
   - User submits the email and password via the form.
2. **Credentials Sent**:
   - `signIn("credentials", { email, password })` sends the data to the backend.
3. **Response Handling**:
   - Responses (success or error) can be programmatically handled.


### Use the SignIn Component in a Nextjs app page

You can now use the SignIn component in a regular page to get access token from your Django-Ninja API.

###### src/app/testsi/page.tsx
```typescript jsx
import {SignIn} from "@/components/auth/sign-in";

export default function Page() {

    return (
        <div>
            <h1>Sign-In Page</h1>
            <SignIn>
            </SignIn>
        </div>
    )
}
```

To check that the data, and the access token is correctly fetched from the API, check your logs. I added a `console.log` 
in the `auth.ts` file that should log the user being returned by the API. In the logs of 
your Nextjs app, you should something as below :

```log
The user being returned:  {
  email: 'your@email.com',
  refresh: 'eyJhbGciXXX',
  access: 'eyJhbGciOXXX'
}
```

Well done! We're getting there :)

### Access the authentification data managed by Auth.js

At our stage, we manage to get tokens from the API using the `authorize` function of the 
Credentials provider provided by Auth.js

We expect Auth.js to store information in the session automatically, and we should be 
able to access it using the Auth.js `useSession`.

Let's modify our page to get the session data. To do so, we firest create a `UserInfo` component as below.

###### src/app/testsi/userinfo.tsx
```typescript jsx
import { auth } from "@/auth"

export default async function UserInfo() {
  const session = await auth()

  return (
      <div>
        {session?.user && <div>
          <h1>User Info</h1>
          <ul>
            {Object.entries(session.user).map(([key, value]) => (
                <li key={key}>
                  <strong>{key}: </strong>
                  {value?.toString() || "N/A"}
                </li>
            ))}
          </ul>
        </div>
        }
      </div>
  )
}
```

And we modify our signin page.

###### src/app/testsi/page.tsx
```typescript jsx
import {SignIn} from "@/components/auth/sign-in";
import { auth } from "@/auth"
import UserInfo from "@/app/testsi/userinfo";


export default async function Page() {
    const session = await auth()
    return (
        <div>
            <h1>Sign-In Page</h1>
            <SignIn></SignIn>
            <UserInfo></UserInfo>
        </div>
    )
}
```

If you enter the credentials, and then refresh the page, you should see the user email appear!
You may want to see the email without a refesh of the page. It is possible, 
but you'll need to transform your `UserInfo` component from a server component to
a client component. 

In a client component, we can't use the `import { auth } from "@/auth"` as we did,
and we need use the `useSession` instead. Let's modify our `UserInfo` component.

###### src/app/testsi/userinfo.tsx
```typescript jsx
"use client"
import {useSession} from "next-auth/react"

export default function UserInfo() {
    const { data: session, status } = useSession();

    if (status === "loading") {
        return <p>Loading...</p>;
    }

    if (!session?.user) {
        return <p>You are not signed in</p>;
    }

    return (
        <div>
            {session?.user && <div>
                <h1>User Info</h1>
                <ul>
                    {Object.entries(session.user).map(([key, value]) => (
                        <li key={key}>
                            <strong>{key}: </strong>
                            {value?.toString() || "N/A"}
                        </li>
                    ))}
                </ul>
            </div>
            }
        </div>
    )
}
```

Doing what's above, you should get this error :
```log
Error: [next-auth]: `useSession` must be wrapped in a <SessionProvider />
```

As explained by the error message, we need to wrap the call to useSession in a SessionProvider.
Simply modify your `layout.tsx` file to add the SessionProvider

###### src/app/layout.tsx
```typescript
import type { Metadata } from "next";
import localFont from "next/font/local";
import "./globals.css";
import RootClientLayout from "@/components/layout/RootClientLayout";
import {Suspense} from "react";
import {SessionProvider} from "next-auth/react";

const geistSans = localFont({
    src: "./fonts/GeistVF.woff",
    variable: "--font-geist-sans",
    weight: "100 900",
});
const geistMono = localFont({
    src: "./fonts/GeistMonoVF.woff",
    variable: "--font-geist-mono",
    weight: "100 900",
});

export const metadata: Metadata = {
    title: "Create Next App",
    description: "Generated by create next app",
};

export default function RootLayout({
                                       children,
                                   }: {
    children: React.ReactNode;
}) {
    return (
        <html lang="en" suppressHydrationWarning>
        <body
            className={`${geistSans.variable} ${geistMono.variable} antialiased`}
        >
        <Suspense fallback={<div>Loading...</div>}>
            <SessionProvider>
                    <RootClientLayout>{children}</RootClientLayout>
            </SessionProvider>
        </Suspense>
        </body>
        </html>
    );
}

```

The important part in the code below the in the wraping of your previous layout in a 
`SessionProvider`. With this, when you signin, you should see the UserInfo appear
dynamically.

### Adding a Sign Out option

Let's add a Sign-out button to our page. You can create a Sign-out component as we did 
for the Sign-in.

###### src/components/auth/sign-out.tsx
```typescript jsx
"use client"
import {signOut} from "next-auth/react";

export default function SignOut() {
    return (
        <button onClick={() => signOut()}>Sign out</button>
    )
}
```

Now modify our page to add the sign-out component.

###### src/app/testsi/page.tsx
```typescript jsx
import {SignIn} from "@/components/auth/sign-in";
import { auth } from "@/auth"
import UserInfo from "@/app/testsi/userinfo";
import SignOut from "@/components/auth/sign-out";


export default async function Page() {
    const session = await auth()
    return (
        <div>
            <h1>Sign-In Page</h1>
            <SignIn></SignIn>
            <SignOut></SignOut>
            <UserInfo></UserInfo>
        </div>
    )
}
```

Et voilà! Clicking the sign-out button should update the `UserInfo` so that it displays 
`You are not signed in`

### Accessing the tokens

While it's nice to be able to get the user email, the initial goal was to get the access 
and refresh tokens and we're not there yet. Let's take care of this.

#### Add callbacks to `auth.js` file.

First, you need to add callbacks to your `auth.js` file.

###### src/auth.ts
```typescript
import NextAuth from "next-auth"
import Credentials from "next-auth/providers/credentials"
import axios from "axios";
import {DJANGO_API_URL} from "@/config/defaults";

export const { handlers, signIn, signOut, auth } = NextAuth({
    providers: [
        Credentials({
            // You can specify which fields should be submitted, by adding keys to the `credentials` object.
            // e.g. domain, username, password, 2FA token, etc.
            credentials: {
                email: {},
                password: {},
            },
            authorize: async (credentials) => {
                try {
                    const response = await axios.post(`${DJANGO_API_URL}/token/pair`, {
                        email: credentials.email,
                        password: credentials.password,
                    });

                    const user = response.data;

                    if (!user || !user.email) {
                        throw new Error("Invalid credentials.");
                    }

                    // Return user object with their profile data
                    console.log("The user being returned: ", user)
                    return user;
                } catch (error) {
                    console.error("Error during authentication:", error);
                    throw new Error("Authentication failed. Please check your credentials.");
                }
            },
        }),
    ],
    callbacks: {
        async jwt({token, user}) {
            return { ...token, ...user };
        },
        async session({session, token, user}) {
            session.user = token as any;
            return session;
        }
    }
})
```

In addition to the existing `Credentials` provider, **callbacks** were added to manage tokens and session behavior. These enable further customization of the authentication process.

##### **Added Callbacks**

1. **`jwt` Callback**:
   - **Purpose**: Modifies the JSON Web Token (JWT) after it's generated.
     - Combines the existing `token` object with the user data returned by the `authorize` method.
     - Ensures that user information is embedded within the token for future use.

2. **`session` Callback**:
   - **Purpose**: Customizes the session object returned to the client.
     - Overrides the default `session.user` with the token data.
     - Ensures that the session includes all necessary user information from the token.

##### **Impact of the Changes**

- **JWT Token Customization**:
  - The `jwt` callback ensures that the user’s data is available in the token for use in subsequent requests.
  
- **Enhanced Session Management**:
  - The `session` callback allows the client to directly access user information via `session.user`, simplifying frontend usage.

##### **Why These Changes Are Important**
- **Security**:
  - These callbacks securely transfer user information via tokens without relying on additional database queries.

- **Customization**:
  - Allows developers to extend and modify authentication flows to suit application-specific needs.

- **Simplified Client-Side Access**:
  - By including user data in the session, client-side components can easily retrieve and display user information.

##### **Summary**
The addition of callbacks enhances the functionality of the authentication process by enabling:
1. Custom JWT token construction (`jwt` callback).
2. Tailored session data for the client (`session` callback).

#### Create a dedicated next-auth types file.

Create a file `next-auth.d.ts` in your `src/types` folder.

```typescript
import NextAuth from 'next-auth';

declare module 'next-auth' {
    interface Session {
        user: {
            email: string;
            access: string;
            refresh: string;
        }
    }
}
```

The `next-auth.d.ts` file defines custom types for NextAuth sessions in a TypeScript application. Here's what this code does:

##### **Purpose**

1. **Type Safety**: Ensures `Session` objects are strongly typed, preventing runtime errors.
2. **Custom Structure**: Adds fields like `email`, `access`, and `refresh` to the `Session.user` object.
3. **Better Developer Experience**: Enables IntelliSense and autocomplete for these custom fields.


##### **How It Works**

- **Module Declaration**: Extends the default `Session` interface from NextAuth to include your custom fields.
- **Automatic Recognition**: TypeScript will pick up the custom type definitions globally.

##### **Benefits**

1. **Consistency**: Enforces a uniform structure for `Session` objects across your app.
2. **Improved Debugging**: Catch type-related errors during development.
3. **Streamlined Usage**: Simplifies working with custom session properties in components or API routes.

Now, you should see additional information returned by your `UserInfo` component, among which
the access and refresh tokens!

### Using the access token

We're almost there. Now let's make a request to the API and attach the access token to see if it works.
I created a new component `UserNames` because I'll use a request that gets my user different names.

###### src/app/testsi/usernames.tsx
```typescript jsx
"use client";

import {DJANGO_API_URL} from "@/config/defaults";
import axios from "axios";
import { useSession } from "next-auth/react";
import { useState } from "react";

export default function UserNames() {
    const { data: session } = useSession();
    const [apiData, setApiData] = useState(null);
    const [error, setError] = useState('');

    const fetchData = async () => {
        if (!session?.user.access) {
            setError("No access token found!");
            return;
        }

        try {
            console.log("Fetching data from: " + `${DJANGO_API_URL}/gambet/me`);
            console.log("DJANGO_API_URL:", DJANGO_API_URL);
            const response = await axios.get(
                `${DJANGO_API_URL}/gambet/me`,
                {
                    headers: {
                        Authorization: `Bearer ${session.user.access}`,
                    },
                }
            );
            setApiData(response.data); // Update state with API response
            setError(''); // Clear any previous errors
        } catch (err) {
            console.error("Error fetching data:", err);
            setError("Failed to fetch data. Please try again.");
        }
    };

    return (
        <div>
            <button onClick={fetchData}>Fetch User Names</button>
            {error && <p style={{ color: "red" }}>{error}</p>}
            {apiData ? (
                <div>
                    <h3>Data from API:</h3>
                    <pre>{JSON.stringify(apiData, null, 2)}</pre>
                </div>
            ) : (
                !error && <p>No data fetched yet.</p>
            )}
        </div>
    );
}

```

I modify my page as below:
###### /src/app/testsi/page.tsx
```typescript jsx
import SignIn from "@/components/auth/sign-in";
import { auth } from "@/auth"
import UserInfo from "@/app/testsi/userinfo";
import SignOut from "@/components/auth/sign-out";
import UserNames from "@/app/testsi/usernames";


export default async function Page() {
    const session = await auth()
    return (
        <div>
            <h1>Sign-In Page</h1>
            <SignIn></SignIn>
            <SignOut></SignOut>
            <UserInfo></UserInfo>
            <UserNames></UserNames>
        </div>
    )
}
```

After cliking the button, it should work! Well done :) 

Also, if you sign out and click on the fecth button, you should have the error `No access token found!`

### Implement the refresh token logic

We've been a long way already, and we're almost there. However, we also need to deal with
the expiration of the access token.

To test it, let's change the validaity of our access token to 10 seconds. 
You need to update the settings of your django app. Add this to the bottom of your file.

###### back: src/config/settings.py
```python
# JWT Auth settings
from datetime import timedelta

NINJA_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(seconds=10)
}
```

Now, if you wait 10 seconds before cliking on the fetch data button, you should get the
error below in your browser console:
```json
{
    "message": "Request failed with status code 401",
    "name": "AxiosError",
    "stack": "Error\n    at captureStackTrace (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/react-dev-overlay/internal/helpers/capture-stack-trace.js:13:23)\n    at console.error (webpack-internal:///(app-pages-browser)/./node_modules/next/dist/client/components/globals/intercept-console-error.js:51:62)\n    at fetchData (webpack-internal:///(app-pages-browser)/./src/app/testsi/usernames.tsx:38:21)",
    "config": {
        [...]
    },
    "code": "ERR_BAD_REQUEST",
    "status": 401
}
```

#### Improve current logic to use hooks

Before implementing the refresh token login, we will improve the current logic so that 
it uses interceptors that will intercept the request and add the access token 
automatically to the request.

##### Create a `lib/axios.ts` file

Start by creating a `axios.ts` file in your `lib` folder.

###### /src/lib/axios.ts
```typescript
import axios from 'axios';
import {DJANGO_API_URL} from "@/config/defaults";

const BASE_URL = DJANGO_API_URL;

export default axios.create({
    baseURL: BASE_URL,
    headers: {'Content-Type': 'application/json'},
});
```

Doing this, in your pages, you can import `axios` from `@/lib/axios` instead of directly
from the axios repository.

Now, we can modify your `UserNames` component as below.

###### src/app/testsi/usernames.tsx
```typescript jsx
"use client";

import axios from "@/lib/axios"
import { useSession } from "next-auth/react";
import { useState } from "react";

export default function UserNames() {
    const { data: session } = useSession();
    const [apiData, setApiData] = useState(null);
    const [error, setError] = useState('');

    const fetchData = async () => {
        if (!session?.user.access) {
            setError("No access token found!");
            return;
        }

        try {
            const response = await axios.get("/gambet/me");
            setApiData(response.data); // Update state with API response
            setError(''); // Clear any previous errors
        } catch (err) {
            console.error("Error fetching data:", err);
            setError("Failed to fetch data. Please try again.");
        }
    };

    return (
        <div>
            <button onClick={fetchData}>Fetch User Names</button>
            {error && <p style={{ color: "red" }}>{error}</p>}
            {apiData ? (
                <div>
                    <h3>Data from API:</h3>
                    <pre>{JSON.stringify(apiData, null, 2)}</pre>
                </div>
            ) : (
                !error && <p>No data fetched yet.</p>
            )}
        </div>
    );
}
```

When trying to fecth data, you should get a 401 error: it was to be expected,
we removed the access code from the header. 

##### Create a hook to automatically add the authorization bearer

Let's create another axios instance that will use a hook.

Start by modifying our `axios.ts` file.

###### src/lib/axios.ts
```typescript
import axios from 'axios';
import {DJANGO_API_URL} from "@/config/defaults";

const BASE_URL = DJANGO_API_URL;

export default axios.create({
    baseURL: BASE_URL,
    headers: {'Content-Type': 'application/json'},
});

export const axiosAuth = axios.create({
    baseURL: BASE_URL,
    headers: {'Content-Type': 'application/json'},
});
```

Now, create a hook for this new axios instance.

###### src/lib/hooks/use-axios-auth.ts
```typescript
"use client"

import {useSession} from "next-auth/react";
import {useEffect} from "react";
import {axiosAuth} from "@/lib/axios";


const useAxiosAuth = () => {
    const {data:session} = useSession();

    useEffect(() => {
        const requestIntercept = axiosAuth.interceptors.request.use(config => {
            if (!config.headers["Authorization"]) {
                config.headers["Authorization"] = `Bearer ${session?.user.access}`;
            }
            return config;
        });

        return () => {
            axiosAuth.interceptors.request.eject(requestIntercept);
        }
    }, [session]);

    return axiosAuth
}

export default useAxiosAuth;
```

1. **Session Integration**:
   - The hook utilizes `useSession` from NextAuth to access the current session data, including the `access` token, which is critical for authenticated API requests.

2. **Request Interceptor**:
   - An Axios request interceptor is added to the `axiosAuth` instance. This interceptor checks every outgoing request:
     - If the `Authorization` header is missing, it adds the `Bearer` token derived from the session's `access` token.
   - This ensures that all API calls made using the `axiosAuth` instance are automatically authenticated.

3. **Reactivity to Session Changes**:
   - The hook listens for changes in the `session` object via the `useEffect` dependency array. If the session changes (e.g., user logs out or token updates), the interceptor adapts accordingly.

4. **Interceptor Cleanup**:
   - The interceptor is removed using the `eject` method during the cleanup phase of `useEffect`. This avoids issues like memory leaks or multiple interceptors being added when the session changes.

5. **Custom Axios Instance**:
   - The `axiosAuth` instance is returned by the hook, allowing it to be used in any component or function. This instance is pre-configured with the logic for automatically appending the access token to outgoing requests.

Finally, let's modify our `UserNames` component.

###### src/app/testsi/usernames.tsx
```typescript jsx
"use client";

import { useSession } from "next-auth/react";
import { useState } from "react";
import useAxiosAuth from "@/lib/hooks/use-axios-auth";

export default function UserNames() {
    const { data: session } = useSession();
    const axiosAuth = useAxiosAuth();
    const [apiData, setApiData] = useState(null);
    const [error, setError] = useState('');

    const fetchData = async () => {
        if (!session?.user.access) {
            setError("No access token found!");
            return;
        }

        try {
            const response = await axiosAuth.get("/gambet/me");
            setApiData(response.data); // Update state with API response
            setError(''); // Clear any previous errors
        } catch (err) {
            console.error("Error fetching data:", err);
            setError("Failed to fetch data. Please try again.");
        }
    };

    return (
        <div>
            <button onClick={fetchData}>Fetch User Names</button>
            {error && <p style={{ color: "red" }}>{error}</p>}
            {apiData ? (
                <div>
                    <h3>Data from API:</h3>
                    <pre>{JSON.stringify(apiData, null, 2)}</pre>
                </div>
            ) : (
                !error && <p>No data fetched yet.</p>
            )}
        </div>
    );
}

```

Note the changes:
1. We are now using `axiosAuth` instead of `axios`
2. We get the `axiosAuth` instance use the newly defined hook

That's all. Now, you should be able to fetch data, as expected... As long as the `access`
token is still valid! Let's take care of that.

#### Add a hook to update the access token with the refresh token

Start by creating a new custom hook to deal with refresh token. 
The `useRefreshToken` hook is designed to handle refreshing the access 
token using the refresh token. 
This ensures that the user remains authenticated without needing to log in 
again when the access token expires.

###### src/lib/hooks/use-refresh-token.ts
```typescript
"use client"

import {useSession} from "next-auth/react";
import axios from "@/lib/axios"


export const useRefreshToken = () => {
    const {data:session} = useSession();

    const refreshToken = async () => {
        const response = await axios.post("/token/refresh", {
            refresh: session?.user.refresh,
        });

        if (session) session.user.access = response.data.access;
    };

    return refreshToken;
}
```

1. **Session Integration**:
   - The hook uses `useSession` from NextAuth to access the current session, including the `refresh` token stored in `session.user.refresh`.

2. **Refresh Token Functionality**:
   - The `refreshToken` function sends a `POST` request to the `/token/refresh` endpoint with the `refresh` token.
   - If the refresh token is valid, the server responds with a new `access` token.

3. **Updating the Access Token**:
   - The new `access` token is assigned to `session.user.access` after a successful response. This updates the session object to use the fresh access token for subsequent requests.

4. **Returning the Function**:
   - The `refreshToken` function is returned from the hook, allowing components or other parts of the app to call it whenever the access token needs to be refreshed.

Finally, modify the previous hook as below.

###### src/lib/hooks/use-axios-auth.ts
```typescript
"use client"

import {useSession} from "next-auth/react";
import {useEffect} from "react";
import {axiosAuth} from "@/lib/axios";
import {useRefreshToken} from "@/lib/hooks/use-refresh-token";


const useAxiosAuth = () => {
    const {data:session} = useSession();
    const refreshToken = useRefreshToken()

    useEffect(() => {
        const requestIntercept = axiosAuth.interceptors.request.use(config => {
                if (!config.headers["Authorization"]) {
                    config.headers["Authorization"] = `Bearer ${session?.user.access}`;
                }
                return config;
            },
            (error) => Promise.reject(error)
        );

        const responseIntercept = axiosAuth.interceptors.response.use(
            (response) => response,
            async (error) => {
                const previousRequest = error.config;
                if (error.response.status === 401 && !previousRequest.sent){
                    previousRequest.sent = true;
                    await refreshToken();
                    previousRequest.headers["Authorization"] = `Bearer ${session?.user.access}`
                    return axiosAuth(previousRequest);
                }
                return Promise.reject(error);
            }
        )

        return () => {
            axiosAuth.interceptors.request.eject(requestIntercept);
            axiosAuth.interceptors.response.eject(responseIntercept);
        }
    }, [session]);

    return axiosAuth
}

export default useAxiosAuth;
```

The main difference in the `useAxiosAuth` hook is the introduction of **response interception** to handle expired access tokens automatically using the `useRefreshToken` hook.

1. **Response Interceptor**:
   - **Purpose**: In v2, a new response interceptor is added to handle `401 Unauthorized` errors.
   - **Behavior**:
     - When a request fails due to an expired token (`401` status), the interceptor attempts to refresh the token using the `useRefreshToken` hook.
     - After refreshing, the original request is retried with the new access token.

2. **Integration with `useRefreshToken`**:
   - The `useRefreshToken` hook is used to fetch a new access token when the current one expires.
   - The refreshed token is dynamically applied to the retried request.

3. **Request Retry Logic**:
   - A new property, `previousRequest.sent`, ensures that each request is retried only once after refreshing the token to prevent infinite loops in case of repeated failures.

4. **Error Handling**:
   - Errors from the response or token refresh process are passed down the promise chain for proper handling.

    
Well done!! Now you're refresh token strategy should work just fine!


##### Check correct implementation

To make sure everything is well set-up, let's add a button to clear the 
fetch data and check the browser console.

###### src/app/testsi/usernames.tsx
```typescript jsx
"use client";

import { useSession } from "next-auth/react";
import { useState } from "react";
import useAxiosAuth from "@/lib/hooks/use-axios-auth";

export default function UserNames() {
    const { data: session } = useSession();
    const axiosAuth = useAxiosAuth();
    const [apiData, setApiData] = useState(null);
    const [error, setError] = useState('');

    const fetchData = async () => {
        if (!session?.user.access) {
            setError("No access token found!");
            return;
        }

        try {
            const response = await axiosAuth.get("/gambet/me");
            setApiData(response.data); // Update state with API response
            setError(''); // Clear any previous errors
        } catch (err) {
            console.error("Error fetching data:", err);
            setError("Failed to fetch data. Please try again.");
        }
    };

    return (
        <div>
            <button onClick={fetchData}>Fetch User Names</button>
            <button onClick={() => setApiData(null)}>Clear Data</button>
            {error && <p style={{ color: "red" }}>{error}</p>}
            {apiData ? (
                <div>
                    <h3>Data from API:</h3>
                    <pre>{JSON.stringify(apiData, null, 2)}</pre>
                </div>
            ) : (
                !error && <p>No data fetched yet.</p>
            )}
        </div>
    );
}
```

We simply added a `Clear Data button` in our `UserNames` component.

To check that everything is working fine:
1. Sign-in
2. Fetch User Data
3. Clear the data
4. Wait 10 seconds
5. Fetch User Data again
    * Data should be fetched correctly
    * In the browser console, you should see an unauthorized GET request: `GET http://127.0.0.1:8000/api/gambet/me 401 (Unauthorized)`

### Recap: Authentication Implementation in Next.js

Here’s a quick summary of the key steps:

#### **1. Setting Up Auth.js**
- **Installed Auth.js**: Configured the Credentials Provider to handle user authentication with email and password.
- **Integrated Django API**: Validated credentials with the Django backend, receiving access and refresh tokens upon successful login.
- **Added Callbacks**:
  - `jwt`: Embedded user information into JWT for subsequent requests.
  - `session`: Customized session data for frontend usage.


#### **2. Building the Sign-In Flow**
- **Sign-In Component**: Created a client-side form for user login, utilizing the `signIn` method from `next-auth/react`.
- **Session Management**: Dynamically accessed user session data to display user information after login.
- **Sign-Out Component**: Enabled users to log out, clearing session data.


#### **3. API Integration with Access Tokens**
- **Access Token Usage**: Demonstrated API requests with the access token appended to the `Authorization` header.
- **Centralized Axios Configuration**: Created a custom `axios` instance to streamline API requests.


#### **4. Handling Access Token Expiry**
- **Refresh Token Logic**:
  - Implemented a `useRefreshToken` hook to automatically refresh the access token when expired.
  - Updated the `useAxiosAuth` hook to include a response interceptor, retrying failed requests after refreshing the token.


#### **5. Testing and Verifying**
- **Dynamic API Requests**:
  - Verified correct behavior by fetching user data from a protected endpoint.
  - Tested token expiration by reducing the access token's lifespan to 10 seconds and confirmed automatic refresh.

#### **Key Takeaways**
- **Seamless Integration**: Combined Auth.js with Django backend for an efficient and secure authentication flow.
- **Automatic Token Management**: Used hooks and interceptors to handle token refreshes transparently.
- **Customizable Session Data**: Leveraged Auth.js callbacks for tailored session management, improving frontend accessibility.

With this setup, your Next.js application now supports a robust, token-based authentication flow, ensuring a seamless and secure user experience.

## Sources

- https://sourcehawk.medium.com/next-auth-with-a-custom-authentication-backend-12c8f54ed4ce
- https://www.youtube.com/watch?v=fYObrr3jf0w&list=WL&index=50&t=2s
- https://www.youtube.com/watch?v=RPl0r-Yl6pU&list=WL&index=49





