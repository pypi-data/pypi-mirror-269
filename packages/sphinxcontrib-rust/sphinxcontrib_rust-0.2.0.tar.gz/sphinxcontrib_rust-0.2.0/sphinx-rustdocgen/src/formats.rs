//! Module for handling the output formats supported.

use std::str::FromStr;

use crate::directives::Directive;
use crate::DirectiveVisibility;

/// Generate title decoration string for RST or fence for MD.
///
/// Args:
///     :ch: The character to use.
///     :len: The length of the decoration required.
///
/// Returns:
///     A string of length ``len`` composed entirely of ``ch``.
fn generate_decoration(ch: char, len: usize) -> String {
    let mut decoration = String::with_capacity(len);
    for _ in 0..len {
        decoration.push(ch);
    }
    decoration
}

/// Supported formats for the docstrings
#[derive(Copy, Clone, Debug, Hash, PartialEq, Eq)]
pub enum Format {
    /// Markdown format
    Md,
    /// reStructuredText format
    Rst,
}

impl Format {
    const MD_VALUES: [&'static str; 3] = ["md", ".md", "markdown"];
    const RST_VALUES: [&'static str; 3] = ["rst", ".rst", "restructuredtext"];

    /// Returns the extension for the format
    pub fn extension(&self) -> &'static str {
        match self {
            Format::Md => Self::MD_VALUES[1],
            Format::Rst => Self::RST_VALUES[1],
        }
    }

    /// Make a format specific document title using the provided title string.
    pub(crate) fn make_title(&self, title: &str, as_code: bool) -> Vec<String> {
        match self {
            Format::Md => {
                vec![
                    if as_code {
                        format!("# `{title}`")
                    }
                    else {
                        format!("# {title}")
                    },
                    String::new(),
                ]
            }
            Format::Rst => {
                let title = if as_code {
                    format!("``{title}``")
                }
                else {
                    title.to_string()
                };
                let decoration = generate_decoration('=', title.len());
                vec![
                    decoration.clone(),
                    title.to_string(),
                    decoration,
                    String::new(),
                ]
            }
        }
    }

    /// Get format specific content for the directive for the output file.
    ///
    /// The function assumes that the directive is the top level directive of
    /// the output file and generates the content accordingly.
    ///
    /// Args:
    ///     :directive: The directive to get the content for, typically a
    ///         ``Crate`` or ``Module`` directive.
    ///
    /// Returns:
    ///     A vec of strings which are the lines of the document.
    pub(crate) fn format_directive<T>(
        &self,
        directive: T,
        max_visibility: &DirectiveVisibility,
    ) -> Vec<String>
    where
        T: RstDirective + MdDirective,
    {
        match self {
            Format::Md => {
                let fence_size = directive.fence_size();
                directive.get_md_text(fence_size, max_visibility)
            }
            Format::Rst => directive.get_rst_text(0, max_visibility),
        }
    }

    /// Get format specific content for the output file.
    ///
    /// This function should not be used for content under a directive.
    ///
    /// Args:
    ///     :content: The content for the file.
    ///
    /// Returns:
    ///     A vec of strings which are the lines of the document.
    pub(crate) fn format_content<T>(&self, content: T) -> Vec<String>
    where
        T: RstContent + MdContent,
    {
        match self {
            Format::Md => content.get_md_text(),
            Format::Rst => content.get_rst_text(""),
        }
    }
}

impl FromStr for Format {
    type Err = ();

    /// Parses the string into an enum value, or panics.
    ///
    /// If the string is ``md``, ``.md`` or ``markdown``, the function
    /// returns ``Md``. If the string is ``rst``, ``.rst`` or
    /// ``restructuredtext``, the function returns ``Rst``. Comparison is
    /// case-insensitive.
    ///
    /// Args:
    ///     :value: The value to parse.
    ///
    /// Returns:
    ///     The parsed enum value as the Ok value, or unit type as the Err.
    fn from_str(value: &str) -> Result<Self, Self::Err> {
        let value_lower = value.to_lowercase();
        if Self::RST_VALUES.contains(&&*value_lower) {
            Ok(Format::Rst)
        }
        else if Self::MD_VALUES.contains(&&*value_lower) {
            Ok(Format::Md)
        }
        else {
            Err(())
        }
    }
}

/// Trait for directives that can be written as RST content
pub(crate) trait RstDirective {
    const INDENT: &'static str = "   ";

    /// Generate RST text with the given level of indentation.
    ///
    /// Implementations must provide a vec of the lines of the content of the
    /// item and all its members.
    ///
    /// Args:
    ///     :level: The level of indentation for the content. Use the
    ///         ``make_indent`` and ``make_content_indent`` functions to get
    ///         the actual indentation string.
    ///     :max_visibility: Include only items with visibility up to the
    ///         defined level.
    ///
    /// Returns:
    ///     The RST text for the documentation of the item and its members.
    fn get_rst_text(self, level: usize, max_visibility: &DirectiveVisibility) -> Vec<String>;

    /// Make a string for indenting the directive.
    ///
    /// Args:
    ///     :level: The level of the indentation.
    ///
    /// Returns:
    ///     A string that is ``Self::INDENT`` repeated ``level`` times.
    fn make_indent(level: usize) -> String {
        let mut indent = String::with_capacity(Self::INDENT.len() * level);
        for _ in 0..level {
            indent += Self::INDENT;
        }
        indent
    }

    /// Make a string for indenting the directive's content and options
    ///
    /// Args:
    ///     :level: The level of the indentation.
    ///
    /// Returns:
    ///     A string that is ``Self::INDENT`` repeated ``level + 1`` times.
    fn make_content_indent(level: usize) -> String {
        let mut indent = String::with_capacity(Self::INDENT.len() * (level + 1));
        for _ in 0..=level {
            indent += Self::INDENT;
        }
        indent
    }

    /// Make the RST directive header from the directive, name and options.
    ///
    /// Args:
    ///     :directive: The RST directive to make the header for.
    ///     :name: The name of the directive.
    ///     :options: The directive options to add.
    ///     :level: The indentation level of the directive.
    ///
    /// Returns:
    ///     A Vec of the directive's header lines.
    fn make_rst_header<O: RstOption>(
        directive: &str,
        name: &str,
        options: &[O],
        level: usize,
    ) -> Vec<String> {
        let indent = &Self::make_indent(level);
        let option_indent = &Self::make_indent(level + 1);
        let mut header = Vec::with_capacity(3 + options.len());
        header.push(String::new());
        header.push(format!("{indent}.. rust:{directive}:: {name}"));
        options
            .iter()
            .for_each(|o| header.push(o.get_rst_text(option_indent)));
        header.push(String::new());
        header
    }

    fn make_rst_toctree(
        indent: &str,
        caption: &str,
        max_depth: Option<u8>,
        dirname: Option<&str>,
        tree: &Vec<&str>,
    ) -> Vec<String> {
        if tree.is_empty() {
            return Vec::new();
        }

        let mut toc_tree = vec![
            String::new(),
            format!("{indent}.. toctree::"),
            format!("{indent}{}:caption: {caption}", Self::INDENT),
        ];
        if let Some(md) = max_depth {
            toc_tree.push(format!("{indent}{}:maxdepth: {md}", Self::INDENT));
        }
        toc_tree.push(String::new());

        let dirname = match dirname {
            None => String::new(),
            Some(d) => format!("{d}/"),
        };
        for &item in tree {
            toc_tree.push(format!("{indent}{}{dirname}{item}", Self::INDENT));
        }
        toc_tree.push(String::new());
        toc_tree
    }

    fn make_rst_section(
        section: &str,
        level: usize,
        items: Vec<Directive>,
        max_visibility: &DirectiveVisibility,
    ) -> Vec<String> {
        let indent = Self::make_indent(level + 1);
        let mut section = vec![
            String::new(),
            format!("{indent}.. rubric:: {section}"),
            String::new(),
        ];
        for item in items {
            section.extend(item.get_rst_text(level + 1, max_visibility))
        }
        // If nothing was added to the section, return empty vec.
        if section.len() > 3 {
            section
        }
        else {
            Vec::new()
        }
    }
}

/// Trait for directives that can be written as MD content
pub(crate) trait MdDirective {
    /// Generate MD text with the given fence size.
    ///
    /// Implementations must provide a vec of the lines of the content of the
    /// item and all its members.
    ///
    /// Args:
    ///     :fence_size: The size of the fence for the directive. Use the
    ///         ``make_fence`` function to get the actual fence string.
    ///     :max_visibility: Include only items with visibility up to the
    ///         defined level.
    ///
    /// Returns:
    ///     The MD text for the documentation of the item and its members.
    fn get_md_text(self, fence_size: usize, max_visibility: &DirectiveVisibility) -> Vec<String>;

    /// Make a string for the fences for the directive.
    ///
    /// Args:
    ///     :fence_size: The size of the fence, must be at least 3.
    ///
    /// Returns:
    ///     A string of colons of length ``fence_size``.
    ///
    /// Panics:
    ///     If the ``fence_size`` is less than 3.
    fn make_fence(fence_size: usize) -> String {
        if fence_size < 3 {
            panic!("Invalid depth for fence: {fence_size}");
        }
        generate_decoration(':', fence_size)
    }

    /// Calculate the fence size required for the item.
    ///
    /// The ``items`` are the members of the current item. So, for
    /// a struct, these will be the list of its fields, for an enum,
    /// the variants, for a module, the items defined in it, etc.
    ///
    /// The fence size for the item is 1 + the max fence size of all
    /// its members. If it has no members, the fence size is 3. So,
    /// the returned value is the minimum fence size required to properly
    /// document the item and its members in Markdown. Depending on the
    /// parent path of the item, the actual fence size used for documentation
    /// may be different, but at least the value returned by this function.
    ///
    /// Args:
    ///     :items: Items which are members of the current item.
    ///
    /// Returns:
    ///     The minimum fence size required to document the item.
    fn calc_fence_size(items: &[Directive]) -> usize {
        match items.iter().map(Directive::fence_size).max() {
            Some(s) => s + 1,
            None => 3,
        }
    }

    /// Make the MD directive header from the directive, name and options.
    ///
    /// Args:
    ///     :directive: The MD directive to make the header for.
    ///     :name: The name of the directive.
    ///     :options: The directive options to add.
    ///     :fence: The fence to use for the directive.
    ///
    /// Returns:
    ///     A Vec of the directive's header lines.
    fn make_md_header<O: MdOption>(
        directive: &str,
        name: &str,
        options: &[O],
        fence: &str,
    ) -> Vec<String> {
        let mut header = Vec::with_capacity(2 + options.len());
        header.push(format!("{fence}{{rust:{directive}}} {name}"));
        options.iter().for_each(|o| header.push(o.get_md_text()));
        header.push(String::new());
        header
    }

    fn make_md_toctree(
        fence_size: usize,
        caption: &str,
        max_depth: Option<u8>,
        dirname: Option<&str>,
        tree: &Vec<&str>,
    ) -> Vec<String> {
        if tree.is_empty() {
            return Vec::new();
        }

        let fence = Self::make_fence(fence_size);
        let mut toc_tree = vec![
            String::new(),
            format!("{fence}.. toctree::"),
            format!(":caption: {caption}"),
        ];
        if let Some(md) = max_depth {
            toc_tree.push(format!(":maxdepth: {md}"));
        }
        toc_tree.push(String::new());
        let dirname = match dirname {
            None => String::new(),
            Some(d) => format!("{d}/"),
        };
        for item in tree {
            toc_tree.push(format!("{dirname}{item}"));
        }
        toc_tree.push(String::new());
        toc_tree
    }

    fn make_md_section(
        section: &str,
        fence_size: usize,
        items: Vec<Directive>,
        max_visibility: &DirectiveVisibility,
    ) -> Vec<String> {
        let fence = Self::make_fence(3);
        let mut section = vec![
            String::new(),
            format!("{fence}{{rubric}} {section}"),
            fence,
            String::new(),
        ];
        for item in items {
            section.extend(item.get_md_text(fence_size - 1, max_visibility))
        }
        // If nothing was added to the section, return empty vec.
        if section.len() > 4 {
            section
        }
        else {
            Vec::new()
        }
    }

    /// Return the fence size required for documenting the item.
    ///
    /// The default implementation returns ``3``, which is the size required
    /// for any item that has no members and the minimum size required by
    /// Markdown.
    ///
    /// Implementations may use ``calc_fence_size`` to override this.
    fn fence_size(&self) -> usize {
        3
    }
}

/// Trait for RST directive options
pub(crate) trait RstOption {
    fn get_rst_text(&self, indent: &str) -> String;
}

/// Trait for MD directive options
pub(crate) trait MdOption {
    fn get_md_text(&self) -> String;
}

/// Trait for anything that can be converted to RST directive content.
///
/// This is implemented for all ``IntoInterator<Item = String>``, effectively
/// allowing ``Vec<String>`` to be converted to RST content lines.
pub(crate) trait RstContent {
    fn get_rst_text(self, indent: &str) -> Vec<String>;
}

impl<T: IntoIterator<Item = String>> RstContent for T {
    fn get_rst_text(self, indent: &str) -> Vec<String> {
        self.into_iter().map(|s| format!("{indent}{s}")).collect()
    }
}

/// Trait for anything that can be converted to MD directive content.
///
/// This is implemented for all ``IntoInterator<Item = String>``, effectively
/// allowing ``Vec<String>`` to be converted to MD content lines.
pub(crate) trait MdContent {
    fn get_md_text(self) -> Vec<String>;
}

impl<T: IntoIterator<Item = String>> MdContent for T {
    fn get_md_text(self) -> Vec<String> {
        self.into_iter().collect()
    }
}
