# Package contains Pre defined functions, which partners can call this by passing inputs


# system and internal libaries
from private_cw_rpa.libraries.common import BotUtils
import subprocess
from types import SimpleNamespace
import re
import requests
import json
import os


# Helps to fetch the resource mailbox properties
def list_resource_mailbox_properties(resource_Mailbox_Name):
    """
    Objective: 
        Fetches properties of a resource mailbox.

    Parameters:
        resource_Mailbox_Name (str): The name of the resource mailbox.

    Description: 
        This function fetches various properties of the specified resource mailbox,
        such as its display name, alias, primary SMTP address, resource type, etc.
    """
    try:
        
        token = BotUtils.generate_access_token()

        try:
            default_domain = BotUtils.get_default_domain(token.access_token_for_graph)
            powershell_command = f"""
            $default_domain = '{default_domain}'
            $resource_Mailbox_Name = '{resource_Mailbox_Name}'
            try {{
            Connect-ExchangeOnline -AccessToken {token.access_token_for_exchange_online} -Organization  $default_domain -ErrorAction Stop -WarningAction SilentlyContinue -ShowBanner:$false
            function fetch_resource_mailbox_properties {{
                param (
                    [string]$mailbox_name
                )

                # Search for the mailbox in the 'roommailbox' category
                $roomMailbox = Get-Mailbox -RecipientTypeDetails roommailbox -Identity $mailbox_name -ErrorAction SilentlyContinue

                # If not found, search in the 'Equipment' category
                if (-not $roomMailbox) {{
                    $roomMailbox = Get-Mailbox -RecipientTypeDetails Equipment -Identity $mailbox_name -ErrorAction SilentlyContinue
                }}

                # If still not found, display an error message and exit the script
                if (-not $roomMailbox) {{
                    Write-Output "[MSG: Resource mailbox not found. Kindly confirm the name '$mailbox_name']"
                    return
                }}

                # Initialize an output string
                $output = @()
                $ErrorActionPreference = 'SilentlyContinue'

                # Add mailbox properties to the output
                $output += "Mailbox General Properties:"
                $output += "-------------------"
                $output += "DisplayName: $($roomMailbox.DisplayName)"
                $output += "Alias: $($roomMailbox.Alias)"
                $output += "PrimarySMTPAddress: $($roomMailbox.PrimarySmtpAddress)"
                $output += "ResourceType: $($roomMailbox.ResourceType)"
                $output += "RoomMailboxAccountEnabled: $($roomMailbox.RoomMailboxAccountEnabled)"
                $output += "UserPrincipalName: $($roomMailbox.UserPrincipalName)"
                $output += "Hide from Global Address List:$($roomMailbox.HiddenFromAddressListsEnabled)"
                $output += ""
                $output += "Mailbox Delegate Properties:"
                $output += "-------------------"
                $calendarProcessing = Get-CalendarProcessing -Identity $roomMailbox
                $output += "Accept booking request automatically: $($calendarProcessing.AutomateProcessing)"
                $output += "Delegate who can accept or decline booking requests: $($calendarProcessing.ResourceDelegates|Get-User|select displayname)"
                $output += "Remove organizer name from subject : $($calendarProcessing.AddOrganizerToSubject)"
                $output += ""
                $output += "Mailbox Booking Properties:"
                $output += "-------------------"
                $calendarProcessing = Get-CalendarProcessing -Identity $roomMailbox
                $output += "Allow repeated meetings: $($calendarProcessing.AllowRecurringMeetings)"
                $output += "Allow scheduling only during working hours: $($calendarProcessing.ScheduleOnlyDuringWorkHours)"
                $output += "Automatically decline meetings outside this limit:"
                $output += "Booking window (days): $($calendarProcessing.BookingWindowInDays)"
                $output += "Maximum duration(hours):$(($calendarProcessing.MaximumDurationInMinutes)/60)"
                $output += "ProcessExternalMeetingMessages: $($calendarProcessing.ProcessExternalMeetingMessages)"
                $output += "Automatically delete Canceled meetings: $($calendarProcessing.RemoveCanceledMeetings)"
                $output += "Meeting organizer to receive a reply text: $($calendarProcessing.AdditionalResponse)"
                $output += ""
                # Add mailbox permissions to the output
                $output += "Mailbox Permissions:"
                $output += "-------------------"
                $output += "Full Access permission:"
                $roomMailboxPermissions = Get-MailboxPermission -Identity $roomMailbox | select Identity, User 
                $output += $roomMailboxPermissions #| Format-Table -AutoSize
                $output += ""
                # Add recipient permissions to the output
                $output += "Send As permission:"
                #$output += "-------------------"
                $recipientPermissions = Get-RecipientPermission -Identity $roomMailbox | select Identity, @{{E = {{ $_.Trustee }}; L = "User" }}
                $output += $recipientPermissions #| Format-Table -AutoSize 
                $output += ""
                $output += "Send on Behalf of permission :"
                #$output += "-------------------"
                $recipientPermissions = Get-Mailbox -Identity $roomMailbox | select -ExpandProperty GrantSendonBehalfTo | Get-User | select displayname | Out-String
                $output += $recipientPermissions #| Format-Table -AutoSize
                $output += "-------------------"
                # Display the formatted output
                $output
            }}
            $result = fetch_resource_mailbox_properties -mailbox_name $resource_Mailbox_Name
            $result | Out-String

            }} catch {{
                Write-Output "[ERROR : An error occurred: $($_.Exception.Message)]"
            }}
            finally {{Disconnect-ExchangeOnline -Confirm:$false}}
            """
            process = subprocess.Popen(
                ["pwsh", "-command", powershell_command],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            output, _ = process.communicate()
            # Check if the error message is present in the command output
            if "ERROR" in output:
                BotUtils.log_error(f"Error processing the request:{output}")
                return False
            else:
                BotUtils.log_result(f"Result:{output}")
                return True

        except Exception as e:
            BotUtils.log_error(f"error occurred: {str(e)}")
            return False

    except Exception as e:
            BotUtils.log_error(f"{e}")
            return False
    
# Helps to create user on 0365
def create_new_o365_user(userPrincipalName, displayName, userPassword):
    """
    Objective: 
        Creates user on o365

    Parameters:
        userPrincipalName : The principal name of the user.
        displayName : The display name of the user.
        password : Password for the user(Strong password recommended).
    Description: 
        This function creates user on o365 
    """
    try:
        token = BotUtils.generate_access_token()
        access_token = token.access_token_for_graph
        try:
            endpoint = "https://graph.microsoft.com/v1.0/users"
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
            }
            req_body = {
                "accountEnabled": True,
                "userPrincipalName": userPrincipalName,
                "mailNickname": re.sub(r"[^a-zA-Z0-9]", "", userPrincipalName),
                "displayName": displayName,
                "passwordProfile": {
                    "forceChangePasswordNextSignIn": True,
                    "password": userPassword,
                },
            }
            data = json.dumps(req_body)
            response = requests.post(url=endpoint, headers=headers, data=data)

            if response.status_code == 201:
                response = response.json()

                #BotUtils.log_result(f"User '{response['userPrincipalName']}' has been successfully created.")
                return True

            elif response.status_code == 400:  # Bad Request
                res_json = response.json()
                if "error" in res_json:
                    if "already exists" in res_json["error"]["message"]:
                        BotUtils.log_error(f"{userPrincipalName} already exist")
                        return False
                    else:
                        BotUtils.log_error("error occured while creating new user.")
                        BotUtils.log_error(res_json["error"]["message"])
                        return False
            elif response.status_code == 404:
                BotUtils.log_error(
                    f"unable to create user. please provide valid input data. \nrequest failed with status code {response.status_code}. Response content: {response.text}"
                )
                return False
            else:
                BotUtils.log_error(
                    f"request failed with status code {response.status_code}. Response content: {response.text}"
                )
                return False

        except Exception as e:
            BotUtils.log_error(f"Failed to get details for user {userPrincipalName}:{e}")
            return False

    except Exception as e:
            BotUtils.log_error(f"{e}")
            return False

