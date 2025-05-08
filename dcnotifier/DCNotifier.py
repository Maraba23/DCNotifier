import json
import traceback
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

import requests


class DCNotifierException(Exception):
    """Base exception for the DCNotifier library."""
    pass


class WebhookError(DCNotifierException):
    """Exception raised when there is an error with the webhook request."""
    def __init__(self, status_code: int, response_text: str):
        self.status_code = status_code
        self.response_text = response_text
        super().__init__(f"Webhook request failed: {status_code} - {response_text}")


class DCNotifier:
    """
    Discord webhook notifier for sending messages and error reports to Discord channels.
    
    Designed to be used in Django applications to send error notifications,
    but can be used in any Python application.
    """
    
    def __init__(self, webhook: str, username: Optional[str] = None, 
                 avatar_url: Optional[str] = None):
        """
        Initialize the Discord notifier.
        
        Args:
            webhook: Discord webhook URL
            username: Override the webhook's default username
            avatar_url: Override the webhook's default avatar
        """
        if not webhook.startswith("https://discord.com/api/webhooks/"):
            raise ValueError("Invalid Discord webhook URL format")
            
        self.webhook_url = webhook
        self.username = username
        self.avatar_url = avatar_url
        self.content = None
        self.embeds = []
        
    def clear(self) -> None:
        """
        Clear all message data to prepare for a new message.
        """
        self.content = None
        self.embeds = []
        
    def set_content(self, content: str) -> 'DCNotifier':
        """
        Set the content for the message.
        
        Args:
            content: Text content of the message
            
        Returns:
            self: For method chaining
        """
        self.content = content
        return self
        
    def set_username(self, username: str) -> 'DCNotifier':
        """
        Set the username for the message.
        
        Args:
            username: Username to display for the message
            
        Returns:
            self: For method chaining
        """
        self.username = username
        return self
        
    def set_avatar_url(self, avatar_url: str) -> 'DCNotifier':
        """
        Set the avatar URL for the message.
        
        Args:
            avatar_url: URL for the avatar image
            
        Returns:
            self: For method chaining
        """
        self.avatar_url = avatar_url
        return self
        
    def add_embed(self, title: Optional[str] = None, description: Optional[str] = None, 
                  color: Optional[int] = None, url: Optional[str] = None, 
                  timestamp: Optional[Union[datetime, str]] = None) -> Dict[str, Any]:
        """
        Add an embed to the message.
        
        Args:
            title: Title of the embed
            description: Description of the embed
            color: Color of the embed in decimal format (e.g. 16711680 for red)
            url: URL to make the title clickable
            timestamp: Timestamp for the embed (ISO8601 format)
            
        Returns:
            embed: The newly created embed dictionary for further customization
        """
        embed = {}
        
        if title:
            embed["title"] = title
        if description:
            embed["description"] = description
        if color:
            embed["color"] = color
        if url:
            embed["url"] = url
            
        if timestamp:
            if isinstance(timestamp, datetime):
                embed["timestamp"] = timestamp.isoformat()
            else:
                embed["timestamp"] = timestamp
                
        self.embeds.append(embed)
        return embed
        
    def add_embed_field(self, embed: Dict[str, Any], name: str, value: str, 
                        inline: bool = False) -> 'DCNotifier':
        """
        Add a field to an embed.
        
        Args:
            embed: The embed to add the field to
            name: Name of the field
            value: Value of the field
            inline: Whether the field should be displayed inline
            
        Returns:
            self: For method chaining
        """
        if "fields" not in embed:
            embed["fields"] = []
            
        embed["fields"].append({
            "name": name,
            "value": value,
            "inline": inline
        })
        
        return self
        
    def set_embed_author(self, embed: Dict[str, Any], name: str, 
                         icon_url: Optional[str] = None, 
                         url: Optional[str] = None) -> 'DCNotifier':
        """
        Set the author for an embed.
        
        Args:
            embed: The embed to set the author for
            name: Name of the author
            icon_url: URL for the author's icon
            url: URL for the author's name
            
        Returns:
            self: For method chaining
        """
        author = {"name": name}
        
        if icon_url:
            author["icon_url"] = icon_url
        if url:
            author["url"] = url
            
        embed["author"] = author
        return self
        
    def set_embed_footer(self, embed: Dict[str, Any], text: str, 
                         icon_url: Optional[str] = None) -> 'DCNotifier':
        """
        Set the footer for an embed.
        
        Args:
            embed: The embed to set the footer for
            text: Text for the footer
            icon_url: URL for the footer's icon
            
        Returns:
            self: For method chaining
        """
        footer = {"text": text}
        
        if icon_url:
            footer["icon_url"] = icon_url
            
        embed["footer"] = footer
        return self
        
    def set_embed_thumbnail(self, embed: Dict[str, Any], url: str) -> 'DCNotifier':
        """
        Set the thumbnail for an embed.
        
        Args:
            embed: The embed to set the thumbnail for
            url: URL for the thumbnail image
            
        Returns:
            self: For method chaining
        """
        embed["thumbnail"] = {"url": url}
        return self
        
    def set_embed_image(self, embed: Dict[str, Any], url: str) -> 'DCNotifier':
        """
        Set the image for an embed.
        
        Args:
            embed: The embed to set the image for
            url: URL for the image
            
        Returns:
            self: For method chaining
        """
        embed["image"] = {"url": url}
        return self

    def prepare_payload(self) -> Dict[str, Any]:
        """
        Prepare the payload for the webhook request.
        
        Returns:
            dict: The payload as a dictionary
        """
        data = {}
        
        if self.username:
            data["username"] = self.username
        if self.avatar_url:
            data["avatar_url"] = self.avatar_url
        if self.content:
            data["content"] = self.content
        if self.embeds:
            data["embeds"] = self.embeds
            
        return data
        
    def send(self) -> bool:
        """
        Send the message to the Discord webhook.
        
        Returns:
            bool: True if the message was sent successfully
            
        Raises:
            WebhookError: If the webhook request fails
        """
        payload = self.prepare_payload()
        
        if not payload.get("content") and not payload.get("embeds"):
            raise DCNotifierException("No content or embeds to send")
            
        try:
            response = requests.post(self.webhook_url, json=payload)
            
            if response.status_code == 204:  # Discord returns 204 No Content on success
                self.clear()
                return True
            else:
                raise WebhookError(response.status_code, response.text)
                
        except requests.RequestException as e:
            raise DCNotifierException(f"Failed to send request: {str(e)}")
    
    def send_message(self, content: Optional[str] = None, 
                    embed_params: Optional[Dict[str, Any]] = None) -> bool:
        """
        Quick method to send a simple message with optional embed.
        
        Args:
            content: Text content of the message
            embed_params: Parameters for an embed
            
        Returns:
            bool: True if the message was sent successfully
        """
        if content:
            self.set_content(content)
            
        if embed_params:
            embed = self.add_embed(**embed_params)
            
            # Add fields if provided
            if "fields" in embed_params:
                for field in embed_params["fields"]:
                    self.add_embed_field(embed, field["name"], field["value"], 
                                        field.get("inline", False))
        
        return self.send()
        
    def notify_error(self, error: Exception, request=None, extra_info: Dict[str, Any] = None,
                    include_traceback: bool = True) -> bool:
        """
        Send an error notification to Discord.
        
        Args:
            error: The exception that was raised
            request: Django request object (optional)
            extra_info: Additional information to include
            include_traceback: Whether to include the traceback
            
        Returns:
            bool: True if the notification was sent successfully
        """
        error_type = type(error).__name__
        error_message = str(error)
        
        # Create main embed for the error
        embed = self.add_embed(
            title=f"❌ Error: {error_type}",
            description=error_message,
            color=16711680,  # Red
            timestamp=datetime.now()
        )
        
        # Add traceback if requested
        if include_traceback:
            tb = traceback.format_exc()
            if len(tb) > 1024:  # Discord field value limit
                tb = tb[:1021] + "..."
            self.add_embed_field(embed, "Traceback", f"```python\n{tb}\n```")
        
        # Add request info if available
        if request:
            try:
                request_info = (
                    f"**Method:** {request.method}\n"
                    f"**Path:** {request.path}\n"
                    f"**User:** {getattr(request, 'user', 'Anonymous')}\n"
                )
                
                # Add query parameters if any
                if request.GET:
                    params = "\n".join([f"- {k}: {v}" for k, v in request.GET.items()])
                    request_info += f"**Query Params:**\n{params}\n"
                
                # Add request body if it's a POST request (with some safety measures)
                if request.method == 'POST' and hasattr(request, 'body'):
                    try:
                        body = request.body.decode('utf-8')
                        # Try to parse as JSON for better formatting
                        try:
                            body_obj = json.loads(body)
                            body = json.dumps(body_obj, indent=2)
                        except json.JSONDecodeError:
                            pass
                        
                        # Truncate if too long
                        if len(body) > 500:
                            body = body[:497] + "..."
                            
                        request_info += f"**Body:**\n```\n{body}\n```"
                    except Exception:
                        request_info += "**Body:** [Could not decode body]"
                
                self.add_embed_field(embed, "Request Information", request_info)
                
            except Exception as e:
                self.add_embed_field(embed, "Request Information", 
                                    f"Error getting request info: {str(e)}")
        
        # Add extra info if provided
        if extra_info:
            extra_info_text = "\n".join([f"**{k}:** {v}" for k, v in extra_info.items()])
            self.add_embed_field(embed, "Additional Information", extra_info_text)
        
        # Add system info
        import platform
        import sys
        
        system_info = (
            f"**Python:** {sys.version.split()[0]}\n"
            f"**Platform:** {platform.platform()}\n"
        )
        
        # Add Django version if available
        try:
            import django
            system_info += f"**Django:** {django.get_version()}\n"
        except ImportError:
            pass
            
        self.add_embed_field(embed, "System Information", system_info)
        
        # Set a meaningful footer
        self.set_embed_footer(embed, "Error occurred at")
        
        return self.send()


# Example usage in Django views:
"""
from django.http import JsonResponse
from .notifications import DCNotifier

notifier = DCNotifier(webhook="https://discord.com/api/webhooks/your_webhook_url")

def my_view(request):
    try:
        # Your view logic here
        result = some_function()
        return JsonResponse({"result": result})
    except Exception as e:
        # Send notification to Discord
        notifier.notify_error(e, request=request)
        # Return appropriate error response
        return JsonResponse({"error": str(e)}, status=500)
"""