"""
File: mkdocs_table_of_figures/plugin.py
Desc: This file contain the plugin used by mkdocs create the table of figures
Author: Thibaud Briard - BRT, <thibaud.brrd@eduge.ch>
Version: 0.1.4 - 2023-05-10
"""
# Imports...
import os, shutil # used to create folder and file in documentation
import subprocess # used to call mermaid cli to prerender diagrams
import re # used to recognize markdown figure pattern
import logging # used to log warning and errors for MkDocs among other things

from mkdocs.config.base import Config as base_config # used to create an MkDocs config class derived from MkDocs config base
from mkdocs.plugins import BasePlugin as base_plugin # used to create an MkDocs plugin class derived from MkDocs plugin base
from mkdocs.config import config_options as c # used for config schema type safety
from mkdocs.structure.files import File # used to create File in documentation

# The plugin config options
class TableOfFiguresConfig(base_config):
    temp_dir = c.Type(str, default='temp_figures')
    file = c.Type(str, default='figures.md')
    title_label = c.Type(str, default='Table of Figures')
    figure_label = c.Type(str, default='Figure')
    description_label = c.Type(str, default='Description')
    follow_nav_structure = c.Type(bool, default=True)
    on_mermaid = c.Type(bool, default=False)
    on_codeblock = c.Type(bool, default=False)
    on_table = c.Type(bool, default=False)

# The plugin itself
class TableOfFigures(base_plugin[TableOfFiguresConfig]):
    def __init__(self):
        self._logger = logging.getLogger('mkdocs.table-of-figures')
        self._logger.setLevel(logging.INFO)

        self.enabled = True
        self.total_time = 0

        self.counter = 1
        self.figures = []
        self.file_directories_count = 0
        self.file_relative_path = ''
        self.page = None
        self.nav_structure = None
        self.docs_dir = None
        #self.mermaid_dir ='assets/mermaids/'
        self.keep_md_format = False
        self.listening = True

    def on_config(self, config):
        self.file_directories_count = self.config.file.count('/')
        self.file_relative_path = '../' * self.file_directories_count
        self.docs_dir = config.docs_dir
        if 'markdown_extensions' in config and 'md_in_html' in config.markdown_extensions:
            self.keep_md_format = True
        return config
    
    def on_nav(self, nav, config, files):
        self.nav_structure = nav
        return

    def on_files(self, files, config):
        tof = os.path.join(self.config.temp_dir, self.config.file)

        # Create directory if it don't exist
        if not os.path.exists(os.path.dirname(tof)):
            os.makedirs(os.path.dirname(tof))

        # Write the title to the tof file
        with open(tof, 'w') as f:
            f.write(f'# {self.config.title_label}\n\n')
        
        # Add the tof file to the mkdocs files list
        self.page = File(self.config.file, src_dir=self.config.temp_dir, dest_dir=config.site_dir, use_directory_urls=config.use_directory_urls)
        files.append(self.page)

        return files
    
    def count_previous_figures(self, page, nav_structure, depth=0):
        found = False
        counter = 0
        depth_range = ''
        for i in range(depth):
            depth_range += '\t'
        
        for index, nav_item in enumerate(nav_structure):
            addon = 0
            if nav_item.is_page:
                if nav_item == page:
                    found = True
                elif os.path.exists(os.path.join(self.docs_dir, nav_item.file.src_uri)):
                    with open(os.path.join(self.docs_dir, nav_item.file.src_uri), 'r') as file:
                        markdown = file.read()

                    pattern_img = r'!\[([^\]]+?)\]\((.+?)\)'
                    pattern_mermaid = r'^(``` ?(mermaid)\r?\n(.*?)```)$\r?\n^([^\n]+?)$'
                    pattern_codeblock = r'^(``` ?([^\r\n]*)\r?\n(.*?)```)$\r?\n^([^\n]+?)$'
                    pattern_table = r'^((?:\|[^|\r\n]*)+\|\r?\n(?:\|[-: ]*)+\|(?:\r?\n(?:\|[^|\r\n]*)+\|)*)\r?\n^([^|\n]+?)$'
                    
                    matches = []
                    matches.extend(re.finditer(pattern_img, markdown, flags= re.IGNORECASE))
                    matches.extend(re.finditer(pattern_mermaid, markdown, flags= re.MULTILINE | re.DOTALL)) if self.config.on_mermaid and not self.config.on_codeblock else None
                    matches.extend(re.finditer(pattern_codeblock, markdown, flags= re.MULTILINE | re.DOTALL)) if self.config.on_codeblock else None
                    matches.extend(re.finditer(pattern_table, markdown, flags= re.MULTILINE | re.DOTALL)) if self.config.on_table else None

                    addon = len(matches)
            elif nav_item.is_section:
                found, addon = self.count_previous_figures(page, nav_item.children, depth + 1)
            
            counter += addon
            if found:
                break
        return found, counter

    def on_page_markdown(self, markdown, page, config, files):
        if self.listening:
            if self.page == page.file:
                self._logger.info(f'Populating table of figure file {self.config.file} with {len(self.figures)} figure{"s" if self.counter else ""} ')
                markdown += f'| {self.config.figure_label} | {self.config.description_label} |\n'
                markdown += f'| -------------------------- | ------------------------------- |\n'
                figures = sorted(self.figures, key=lambda figure: figure["number"])
                for figure in figures:
                    markdown += f'| [{self.config.figure_label} {figure["number"]}]({figure["link"]}) | {figure["description"]} |\n'
                
                self.listening = False
            else:
                if self.config.follow_nav_structure and self.nav_structure:
                    found, counter = self.count_previous_figures(page, self.nav_structure)
                    if found:
                        self.counter = counter + 1

                original = markdown
                try:
                    pattern_img = r'!\[(.*?)\]\((.+?)\)'
                    pattern_mermaid = r'^(``` ?(mermaid)\r?\n(.*?)```)$\r?\n^(.*?)$'
                    pattern_codeblock = r'^(``` ?([^\r\n]*)\r?\n(.*?)```)$\r?\n^(.*?)$'
                    pattern_table = r'^((?:\|[^|\r\n]*)+\|\r?\n(?:\|[-: ]*)+\|(?:\r?\n(?:\|[^|\r\n]*)+\|)*)\r?\n^([^|]*?)$'
                    
                    matches = []
                    matches.extend(re.finditer(pattern_img, markdown, flags= re.IGNORECASE))
                    matches.extend(re.finditer(pattern_mermaid, markdown, flags= re.MULTILINE | re.DOTALL)) if self.config.on_mermaid and not self.config.on_codeblock else None
                    matches.extend(re.finditer(pattern_codeblock, markdown, flags= re.MULTILINE | re.DOTALL)) if self.config.on_codeblock else None
                    matches.extend(re.finditer(pattern_table, markdown, flags= re.MULTILINE | re.DOTALL)) if self.config.on_table else None
                    matches = sorted(matches, key=lambda x: x.start())

                    position_offset = 0
                    for match in matches:
                        checkpoint = markdown

                        try:
                            link = f'{self.file_relative_path}{page.file.src_uri}#figure-{self.counter}'
                            replacement = match.group(0)
                            if match.re.pattern == pattern_img and match.group(1):
                                self.figures.append({"number": self.counter, "description": match.group(1), "link": link})
                                replacement = f'<figure id="figure-{self.counter}" class="figure-image" markdown="span">\n  <img src="{config.site_url + match.group(2) if match.group(2).startswith("/") else match.group(2)}" alt="{match.group(1)}">\n  <figcaption>{self.config.figure_label} {self.counter} — {match.group(1)}</figcaption>\n</figure>'
                                if self.keep_md_format:
                                    replacement = f'<figure id="figure-{self.counter}" class="figure-image" markdown="span">\n![{match.group(1)}]({match.group(2)})\n<figcaption>{self.config.figure_label} {self.counter} — {match.group(1)}</figcaption>\n</figure>'
                            elif (match.re.pattern == pattern_mermaid and match.group(4)) or (self.config.on_mermaid and match.re.pattern == pattern_codeblock and match.group(2) == 'mermaid' and match.group(4)):
                                self.figures.append({"number": self.counter, "description": match.group(4), "link": link})
                                replacement = f'<figure id="figure-{self.counter}" class="figure-mermaid" markdown>\n{match.group(1)}\n<figcaption>{self.config.figure_label} {self.counter} — {match.group(4)}</figcaption>\n</figure>'
                            elif match.re.pattern == pattern_codeblock and match.group(2) != 'mermaid' and match.group(4):
                                self.figures.append({"number": self.counter, "description": match.group(4), "link": link})
                                replacement = f'<figure id="figure-{self.counter}" class="figure-codeblock" markdown>\n{match.group(1)}\n<figcaption>{self.config.figure_label} {self.counter} — {match.group(4)}</figcaption>\n</figure>'
                            elif match.re.pattern == pattern_table and match.group(2):
                                self.figures.append({"number": self.counter, "description": match.group(2), "link": link})
                                replacement = f'<figure id="figure-{self.counter}" class="figure-table" markdown>\n{match.group(1)}\n<figcaption>{self.config.figure_label} {self.counter} — {match.group(2)}</figcaption>\n</figure>'
                            
                            if replacement == match.group(0):
                                self._logger.debug(f'Ignoring image/diagram at {self.file_relative_path}{page.file.src_uri}')
                            else:
                                self._logger.debug(f'Formating image/diagram as figure at {self.file_relative_path}{page.file.src_uri}')
                                self.counter += 1
                                markdown = markdown[:match.start() + position_offset] + replacement + markdown[match.end() + position_offset:]
                                position_offset += len(replacement) - len(match.group(0))
                        except Exception as error:
                            self._logger.warning(error)
                            markdown = checkpoint
                            
                except Exception as error:
                    self._logger.warning(error)
                    markdown = original

        return markdown
    
    
    def on_post_build(self, config):
        # Removing temp_dir directory
        self._logger.info(f'Removing tables of figure temporary directory {self.config.temp_dir}')
        if os.path.exists(self.config.temp_dir):
            shutil.rmtree(self.config.temp_dir)
        return
