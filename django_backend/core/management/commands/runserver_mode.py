from django.core.management.commands.runserver import Command as RunServerCommand
import os


class Command(RunServerCommand):
    help = "Run the server with specified debug mode"

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            "--mode",
            choices=["debug", "prod"],
            default="debug",
            help="Specify the server mode (debug/prod)",
        )

    def handle(self, *args, **options):
        mode = options.get("mode", "debug")
        if mode == "prod":
            os.environ["DEBUG"] = "False"
        else:
            os.environ["DEBUG"] = "True"
        super().handle(*args, **options)
